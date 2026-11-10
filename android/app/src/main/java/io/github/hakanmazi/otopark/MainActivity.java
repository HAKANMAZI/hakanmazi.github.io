package io.github.hakanmazi.otopark;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.core.content.FileProvider;
import androidx.webkit.WebViewAssetLoader;

import java.io.File;

/**
 * Otopark uygulaması: APK'nın içindeki web uygulamasını (assets/index.html) tam ekran gösterir.
 * Fotoğraf ve videolar telefonun içinde, uygulamanın kendi depolamasında (IndexedDB) saklanır.
 */
public class MainActivity extends Activity {
    // Uygulama dosyaları bu sabit adresten sunulur; böylece kayıtlar hep aynı yerde kalır.
    private static final String START_URL = "https://appassets.androidplatform.net/assets/index.html";
    private static final int REQ_CAPTURE = 1;

    private WebView webView;
    private ValueCallback<Uri[]> pendingCallback;
    private Uri pendingUri;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.parseColor("#1565c0"));
        cleanOldCaptures();

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        webView = new WebView(this);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return loader.shouldInterceptRequest(request.getUrl());
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            // Sayfadaki "Fotoğraf" / "Video" butonları buraya gelir: kamerayı açarız
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (pendingCallback != null) pendingCallback.onReceiveValue(null);
                pendingCallback = callback;

                boolean video = false;
                for (String t : params.getAcceptTypes()) if (t != null && t.startsWith("video")) video = true;

                try {
                    File dir = new File(getCacheDir(), "captures");
                    dir.mkdirs();
                    File out = new File(dir, System.currentTimeMillis() + (video ? ".mp4" : ".jpg"));
                    pendingUri = FileProvider.getUriForFile(MainActivity.this,
                            "io.github.hakanmazi.otopark.files", out);

                    Intent i = new Intent(video ? MediaStore.ACTION_VIDEO_CAPTURE : MediaStore.ACTION_IMAGE_CAPTURE);
                    i.putExtra(MediaStore.EXTRA_OUTPUT, pendingUri);
                    i.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    startActivityForResult(i, REQ_CAPTURE);
                    return true;
                } catch (ActivityNotFoundException e) {
                    // Kamera uygulaması yoksa dosya seçiciyi aç
                    try {
                        pendingUri = null;
                        startActivityForResult(params.createIntent(), REQ_CAPTURE);
                        return true;
                    } catch (ActivityNotFoundException e2) {
                        pendingCallback = null;
                        return false;
                    }
                }
            }
        });

        setContentView(webView);
        if (savedInstanceState != null) webView.restoreState(savedInstanceState);
        else webView.loadUrl(START_URL);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != REQ_CAPTURE || pendingCallback == null) return;
        Uri[] result = null;
        if (resultCode == RESULT_OK) {
            if (pendingUri != null) {
                // Bazı kamera uygulamaları videoyu kendi seçtiği yere kaydedip adresini döndürür
                Uri returned = data != null ? data.getData() : null;
                File f = new File(new File(getCacheDir(), "captures"), pendingUri.getLastPathSegment());
                result = new Uri[]{ (f.exists() && f.length() > 0) || returned == null ? pendingUri : returned };
            } else if (data != null && data.getData() != null) {
                result = new Uri[]{ data.getData() };
            }
        }
        pendingCallback.onReceiveValue(result);
        pendingCallback = null;
        pendingUri = null;
    }

    // Kamera geçici dosyaları: kayıt uygulamanın içine kopyalandıktan sonra gereksiz, 1 günden eskileri sil
    private void cleanOldCaptures() {
        File[] files = new File(getCacheDir(), "captures").listFiles();
        if (files == null) return;
        long limit = System.currentTimeMillis() - 24L * 60 * 60 * 1000;
        for (File f : files) if (f.lastModified() < limit) f.delete();
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        webView.saveState(outState);
    }

    @Override
    public void onBackPressed() {
        // Tam ekran fotoğraf açıksa geri tuşu onu kapatsın
        webView.evaluateJavascript(
                "(function(){var v=document.getElementById('viewer');" +
                "if(v&&v.classList.contains('open')){v.classList.remove('open');return 1}return 0})()",
                r -> { if (!"1".equals(r)) finish(); });
    }
}
