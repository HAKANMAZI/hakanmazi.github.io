import math, subprocess, numpy as np, wave, random
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1280,720,30
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s,b=False): return ImageFont.truetype(FB if b else F,s)
fT,fH,fM,fS,fX=font(64,1),font(40,1),font(28),font(22),font(18)
OUT="/home/user/hakanmazi.github.io/hipersonik"
# background
yy=np.linspace(0,1,H)[:,None]
bg=np.zeros((H,W,3),np.uint8)
bg[...,0]=(8+10*yy); bg[...,1]=(14+18*yy); bg[...,2]=(30+30*yy)
random.seed(3)
BG=Image.fromarray(bg); d=ImageDraw.Draw(BG)
for _ in range(160):
    x,y=random.randint(0,W),random.randint(0,H); c=random.randint(80,200); d.point((x,y),fill=(c,c,c+30))
CY=(255,200,60); BL=(110,190,255); OR=(255,140,50); WH=(235,240,250); GR=(150,160,180); RD=(255,80,70)
def cl(x,a=0,b=1): return max(a,min(b,x))
def ease(x): x=cl(x); return x*x*(3-2*x)
def fade(t,s,d=0.6): return ease((t-s)/d)
def col(c,a): return c+(int(255*cl(a)),)
def text(dr,xy,s,f,c,a=1,anchor="la"): 
    if a>0.01: dr.text(xy,s,font=f,fill=col(c,a),anchor=anchor)
def missile(dr,x,y,ang,sc=1,c=(210,215,225),a=1):
    pts=[(40,0),(22,-6),(-30,-6),(-38,-14),(-38,14),(-30,6),(22,6)]
    ca,sa=math.cos(ang),math.sin(ang)
    P=[(x+sc*(px*ca-py*sa),y+sc*(px*sa+py*ca)) for px,py in pts]
    dr.polygon(P,fill=col(c,a))
def glow(dr,x,y,r,c,a=1):
    for i in range(6,0,-1):
        rr=r*i/6; dr.ellipse((x-rr,y-rr,x+rr,y+rr),fill=col(c,a*0.12))
def header(dr,t,s,sub=None):
    a=fade(t,0); text(dr,(60,50),s,fH,CY,a)
    dr.rectangle((60,104,60+int(220*a),108),fill=col(CY,a))
    if sub: text(dr,(60,120),sub,fS,GR,fade(t,0.3))

def s_title(dr,t,D):
    # missile streak
    p=ease(t/5); x=-100+p*(W+250); y=430-120*p
    for i in range(40):
        q=i/40; dr.line((x-q*600,y+q*600*120/1350, x-(q+0.03)*600,y+(q+0.03)*600*120/1350),fill=col(OR,0.6*(1-q)),width=int(10*(1-q))+1)
    glow(dr,x+30,y-3,40,OR,0.9); missile(dr,x,y,math.atan2(-120,1350),1.6)
    text(dr,(W/2,250),"HİPERSONİK FÜZELER",fT,WH,fade(t,0.8),"mm")
    text(dr,(W/2,320),"Ses hızının 5 katından hızlı giden bir füze nasıl çalışır?",fM,CY,fade(t,1.6),"mm")
    text(dr,(W/2,660),"Bilgilendirici kısa video",fS,GR,fade(t,2.4),"mm")

def s_mach(dr,t,D):
    header(dr,t,"Mach 5 nedir?","Mach 1 = ses hızı ≈ 1.235 km/sa (deniz seviyesinde)")
    rows=[("Yolcu uçağı","Mach 0,85  ~900 km/sa",0.85,GR),("Concorde","Mach 2  ~2.180 km/sa",2.0,BL),
          ("Mermi (tüfek)","Mach 2,5–3",2.8,(170,140,255)),("Hipersonik füze","Mach 5+  >6.000 km/sa",5.0,OR)]
    for i,(n,v,m,c) in enumerate(rows):
        y=200+i*85; a=fade(t,0.8+i*0.7); g=ease((t-0.8-i*0.7)/1.5)
        text(dr,(60,y+10),n,fM,WH,a)
        dr.rectangle((330,y,330+int(m/6*780*g),y+46),fill=col(c,a))
        text(dr,(340+int(m/6*780*g),y+10),v if g>0.95 else "",fS,WH,a)
    x0=330+int(780/5)
    for k in range(1,7):
        xx=330+int(780*k/6); dr.line((xx,190,xx,540),fill=col(GR,0.25*fade(t,0.5)),width=1)
        text(dr,(xx,555),f"M{k}",fX,GR,fade(t,0.5),"mm")
    text(dr,(W/2,630),"Saniyede ~1,7 km → İstanbul–Ankara (~350 km) yaklaşık 3,5 dakikada!",fM,CY,fade(t,5.5),"mm")

GROUND=600
def s_hgv(dr,t,D):
    header(dr,t,"Tip 1: Hipersonik Süzülme Aracı (HGV)","Hypersonic Glide Vehicle — roketle fırlatılır, motorsuz süzülür")
    dr.rectangle((0,GROUND,W,H),fill=(20,30,40)); dr.line((0,GROUND,W,GROUND),fill=GR,width=2)
    dr.line((0,300,W,300),fill=col(BL,0.3),width=1); text(dr,(W-20,290),"atmosferin üst sınırı (~100 km)",fX,BL,0.6,"rs")
    # ballistic reference
    if t>8:
        pts=[(100+i*10, GROUND-380*math.sin(math.pi*i/110)) for i in range(111)]
        a=fade(t,8)
        for i in range(0,110,2): dr.line(pts[i]+pts[i+1],fill=col(GR,0.6*a),width=2)
        text(dr,(650,205),"Balistik füze: yüksek ve tahmin edilebilir yay",fS,GR,a,"mm")
    def path(u):  # 0..1 launch-> boost -> glide
        if u<0.25: v=u/0.25; return 100+80*v, GROUND-330*ease(v)**0.8
        v=(u-0.25)/0.75; x=180+v*(1000); y=GROUND-330+v*170+28*math.sin(v*14)*(1-v)
        if v>0.85: y+= (v-0.85)/0.15*120
        return x,y
    u=cl((t-1)/9); pts=[path(k/200*u) for k in range(201)]
    for i in range(200): dr.line(pts[i]+pts[i+1],fill=col(OR if i/200*u>0.25 else CY,0.85),width=3)
    x,y=pts[-1]; x2,y2=path(min(1,u+0.005)); ang=math.atan2(y2-y,x2-x)
    if u<1 and t>1:
        if u<0.25: missile(dr,x,y,ang,1.4); glow(dr,x-40*math.cos(ang),y-40*math.sin(ang),25,OR)
        else:
            glow(dr,x,y,30,OR,0.8); dr.polygon([(x+22*math.cos(ang),y+22*math.sin(ang)),(x-18*math.cos(ang)-9*math.sin(ang),y-18*math.sin(ang)+9*math.cos(ang)),(x-18*math.cos(ang)+9*math.sin(ang),y-18*math.sin(ang)-9*math.cos(ang))],fill=WH)
    if t>3.2 and t<6: bx,by=path(0.25); fy=by+(t-3.2)*120; missile(dr,bx-10,fy,math.pi/2,1.1,(130,130,140),cl(1-(t-3.2)/2.8))
    steps=["1) Roket güçlendirici aracı çok yükseğe ve hızla çıkarır","2) Süzülme aracı ayrılır, motor düşer",
           "3) Atmosferin üst katmanında Mach 5–20 ile süzülür, sekerek manevra yapar"]
    for i,s in enumerate(steps): text(dr,(60,615+i*32),s,fS,WH,fade(t,1+i*2.6))
    text(dr,(W-30,140),"Örnekler: Avangard (Rusya), DF-17 (Çin)",fS,GR,fade(t,11),"rm")

def s_scram(dr,t,D):
    header(dr,t,"Tip 2: Scramjet Motorlu Seyir Füzesi","Supersonic Combustion Ramjet — hava akışı süpersonik hızdayken yanma")
    oy=400
    top=[(160,oy-130),(1120,oy-130),(1120,oy-60),(980,oy-60),(560,oy-60),(380,oy-40)]
    # body shape: upper wall and lower inlet ramp
    up=[(150,oy-140),(1150,oy-140),(1150,oy-100),(1000,oy-70),(800,oy-55),(450,oy-55),(150,oy-120)]
    lo=[(250,oy+120),(450,oy+55),(800,oy+55),(1000,oy+80),(1150,oy+120),(1150,oy+140),(300,oy+140)]
    a=fade(t,0.3)
    dr.polygon(up,fill=col((70,80,100),a)); dr.polygon(lo,fill=col((70,80,100),a))
    dr.rectangle((800,oy-55,1000,oy-48),fill=col(OR,a*0.6)); 
    for fx in range(820,990,40): dr.ellipse((fx-4,oy-50,fx+4,oy-42),fill=col(CY,a))
    random.seed(1); tt=t*1.0
    for k in range(260):
        ph=random.random(); ly=random.uniform(-1,1); sp=random.uniform(0.8,1.2)
        q=(ph+tt*0.25*sp)%1; x=60+q*1180
        if x<450: half=150-(x-60)/(390)*95
        elif x<1000: half=55+ (x-800)/200*20 if x>800 else 55
        else: half=75+(x-1000)/150*55
        y=oy+ly*(half-6)
        if x<800: c=BL
        elif x<1000: c=OR
        else: c=RD
        L=14 if x<800 else 18
        dr.line((x-L,y,x,y),fill=col(c,0.8*a),width=2)
    labs=[(300,"GİRİŞ","Hava şok dalgalarıyla","sıkıştırılır (hareketli parça yok)",BL,1.5),
          (830,"YANMA ODASI","Yakıt süpersonik hava","akışında yanar",OR,4),
          (1130,"LÜLE","Genleşen sıcak gaz","itki üretir",RD,6.5)]
    for x,h,l1,l2,c,s in labs:
        aa=fade(t,s); xx=x
        text(dr,(xx,200),h,fM,c,aa,"mm"); text(dr,(xx,560),l1,fS,WH,aa,"mm"); text(dr,(xx,588),l2,fS,WH,aa,"mm")
    text(dr,(W/2,655),"Scramjet ancak ~Mach 4+ hızda çalışır → füze önce roketle hızlandırılır",fS,CY,fade(t,9),"mm")
    text(dr,(W/2,688),"Örnekler: Zirkon (Rusya), X-51A Waverider (ABD test aracı)",fX,GR,fade(t,10.5),"mm")

def s_heat(dr,t,D):
    header(dr,t,"En büyük düşman: ISI","Havayı bu hızda yarmak, yüzeyi aşırı ısıtır")
    cx,cy=430,400; g=ease((t-0.5)/6)
    # shock cone
    for i in range(10,0,-1):
        c=(int(255),int(80+140*(1-i/10)),int(40*(1-i/10)))
        dr.polygon([(cx+260,cy),(cx-200,cy-30-i*14*g),(cx-200,cy+30+i*14*g)],fill=col(c,0.06+0.05*g))
    glow(dr,cx+230,cy,60+60*g,(255,190,90),0.9*g)
    missile(dr,cx,cy,0,5.5,(200,205,215))
    temp=int(20+2180*g); tc=(255,int(255-170*g),int(255-220*g))
    text(dr,(cx,cy+170),f"{temp:,} °C".replace(",","."),fT,tc,fade(t,0.5),"mm")
    bl=["• Hava sıkışması ve sürtünme yüzeyi 2.000 °C'nin üzerine ısıtır",
        "• Etrafında plazma katmanı oluşur → radyo iletişimi zorlaşır",
        "• Çözüm: karbon-karbon kompozitler, seramik ısı kalkanları",
        "• Yön bulma: ataletsel seyir + uydu + gelişmiş sensörler"]
    for i,s in enumerate(bl): text(dr,(760,240+i*70),s.split(" → ")[0][:48],fS,WH,fade(t,2+i*1.8)) if False else None
    for i,s in enumerate(bl):
        import textwrap
        for j,ln in enumerate(textwrap.wrap(s,36)): text(dr,(780,200+i*110+j*30),ln,fS,WH,fade(t,2+i*1.8))

def s_def(dr,t,D):
    header(dr,t,"Neden durdurmak çok zor?","Hız + alçak irtifa + manevra = çok kısa tepki süresi")
    # earth curve
    R=3000; ex,ey=W/2,GROUND+R-40
    dr.ellipse((ex-R,ey-R,ex+R,ey+R),fill=(20,34,44),outline=GR)
    rx,ry=1130,GROUND-70+10
    dr.polygon([(rx-20,ry+8),(rx+20,ry+8),(rx,ry-20)],fill=WH); text(dr,(rx,ry+34),"Radar",fX,WH,1,"mm")
    # radar horizon line (tangent)
    a=fade(t,0.5); dr.line((rx,ry-20,150,ry-170),fill=col(BL,0.5*a),width=2)
    text(dr,(300,ry-195),"radar görüş sınırı",fX,BL,a,"mm")
    u=cl((t-1)/7)
    # ballistic
    bp=[(80+i*9,GROUND-60-300*math.sin(math.pi*i/110)) for i in range(int(110*u)+1)]
    for i in range(len(bp)-1): dr.line(bp[i]+bp[i+1],fill=col(GR,0.8),width=3)
    # hypersonic low
    hp=[(80+i*9,GROUND-110-40*math.sin(i/9)*(1-i/110)+ (i/110)**4*0) for i in range(int(110*u)+1)]
    for i in range(len(hp)-1): dr.line(hp[i]+hp[i+1],fill=col(OR,0.95),width=3)
    if len(bp)>1:
        glow(dr,*bp[-1],12,WH,0.7)
        # detection markers
        if bp[-1][1]<ry-20-(rx-bp[-1][0])*150/980 : text(dr,(bp[-1][0],bp[-1][1]-25),"erken tespit ✓",fX,(120,230,140),1,"mm")
        glow(dr,*hp[-1],16,OR,0.9)
        lim=ry-20-(rx-hp[-1][0])*150/(rx-150)
        text(dr,(hp[-1][0],hp[-1][1]+28),"geç tespit!" if hp[-1][1]<lim else "görünmüyor",fX,RD,1,"mm")
    bl=["• Alçak uçtuğu için radar ufkunun altında kalır","• Sürekli manevra → yörünge tahmin edilemez","• Tespitten çarpmaya kadar sadece birkaç dakika"]
    for i,s in enumerate(bl): text(dr,(60,162+i*30),s,fS,WH,fade(t,4+i*1.8))

def s_end(dr,t,D):
    text(dr,(W/2,140),"ÖZET",fH,CY,fade(t,0),"mm")
    L=["Hipersonik = Mach 5'ten hızlı (>6.000 km/sa)",
       "HGV: roketle yükselir, atmosferde süzülerek manevra yapar",
       "Scramjet: süpersonik hava akışında yakıt yakan motor",
       "En büyük zorluk: 2.000 °C+ ısı ve malzeme",
       "Avantajı: hız + manevra = savunması çok zor"]
    for i,s in enumerate(L): text(dr,(W/2,230+i*60),s,fM,WH,fade(t,0.6+i*0.7),"mm")
    text(dr,(W/2,640),"İzlediğiniz için teşekkürler",fS,GR,fade(t,5),"mm")

scenes=[(s_title,7),(s_mach,13),(s_hgv,15),(s_scram,15),(s_heat,13),(s_def,13),(s_end,9)]
total=sum(d for _,d in scenes)
# audio
sr=44100; n=int(total*sr); tt=np.arange(n)/sr
aud=0.12*np.sin(2*np.pi*55*tt)+0.08*np.sin(2*np.pi*82.4*tt+np.sin(tt*0.3))+0.05*np.sin(2*np.pi*110*tt)
aud*=0.6+0.4*np.sin(2*np.pi*tt/8)**2
noise=np.random.default_rng(0).normal(0,1,n); 
wh=np.exp(-((tt-2.5)/1.2)**2)*np.convolve(noise,np.ones(40)/40,'same')*0.6
aud=aud+wh; env=np.minimum(1,np.minimum(tt/2,(total-tt)/3)); aud*=env
pcm=(np.clip(aud,-1,1)*20000).astype(np.int16)
with wave.open(OUT+"/ses.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",OUT+"/ses.wav",
  "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-preset","medium","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",OUT+"/hipersonik-fuzeler.mp4"],stdin=subprocess.PIPE)
for fn,D in scenes:
    for k in range(int(D*FPS)):
        t=k/FPS; img=BG.copy(); dr=ImageDraw.Draw(img,"RGBA"); fn(dr,t,D)
        f=min(1,t/0.5,(D-t)/0.5)
        if f<1: dr.rectangle((0,0,W,H),fill=(0,0,0,int(255*(1-f))))
        p.stdin.write(img.tobytes())
p.stdin.close(); p.wait()
import os; os.remove(OUT+"/ses.wav")
# preview frames
