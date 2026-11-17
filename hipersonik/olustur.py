import math, subprocess, numpy as np, wave, random, sys, os, textwrap
from PIL import Image, ImageDraw, ImageFont
LANG=sys.argv[1]; VD=sys.argv[2]; OUT=sys.argv[3]
W,H,FPS=1280,720,30
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s,b=False): return ImageFont.truetype(FB if b else F,s)
fT,fH,fM,fS,fX=font(64,1),font(40,1),font(28),font(22),font(18)
TX={
'tr':dict(
 title="HİPERSONİK FÜZELER",tsub="Ses hızının 5 katından hızlı giden bir füze nasıl çalışır?",tsmall="Bilgilendirici kısa video",
 mach_h="Mach 5 nedir?",mach_s="Mach 1 = ses hızı ≈ 1.235 km/sa (deniz seviyesinde)",
 rows=[("Yolcu uçağı","Mach 0,85  ~900 km/sa"),("Concorde","Mach 2  ~2.180 km/sa"),("Mermi (tüfek)","Mach 2,5–3"),("Hipersonik füze","Mach 5+  >6.000 km/sa")],
 mach_b="Saniyede ~1,7 km → İstanbul–Ankara (~350 km) yaklaşık 3,5 dakikada!",
 hgv_h="Tip 1: Hipersonik Süzülme Aracı (HGV)",hgv_s="Hypersonic Glide Vehicle — roketle fırlatılır, motorsuz süzülür",
 atm="atmosferin üst sınırı (~100 km)",bal="Balistik füze: yüksek ve tahmin edilebilir yay",
 hgv_steps=["1) Roket güçlendirici aracı çok yükseğe ve hızla çıkarır","2) Süzülme aracı ayrılır, motor düşer","3) Atmosferin üst katmanında Mach 5–20 ile süzülür, sekerek manevra yapar"],
 hgv_ex="Örnekler: Avangard (Rusya), DF-17 (Çin)",
 sc_h="Tip 2: Scramjet Motorlu Seyir Füzesi",sc_s="Supersonic Combustion Ramjet — hava akışı süpersonik hızdayken yanma",
 sc_l=[("GİRİŞ","Hava şok dalgalarıyla","sıkıştırılır (hareketli parça yok)"),("YANMA ODASI","Yakıt süpersonik hava","akışında yanar"),("LÜLE","Genleşen sıcak gaz","itki üretir")],
 sc_b="Scramjet ancak ~Mach 4+ hızda çalışır → füze önce roketle hızlandırılır",sc_ex="Örnekler: Zirkon (Rusya), X-51A Waverider (ABD test aracı)",
 ht_h="En büyük düşman: ISI",ht_s="Havayı bu hızda yarmak, yüzeyi aşırı ısıtır",thou=".",
 ht_b=["• Hava sıkışması ve sürtünme yüzeyi 2.000 °C'nin üzerine ısıtır","• Etrafında plazma katmanı oluşur → radyo iletişimi zorlaşır","• Çözüm: karbon-karbon kompozitler, seramik ısı kalkanları","• Yön bulma: ataletsel seyir + uydu + gelişmiş sensörler"],
 df_h="Neden durdurmak çok zor?",df_s="Hız + alçak irtifa + manevra = çok kısa tepki süresi",radar="Radar",rh="radar görüş sınırı",
 early="erken tespit ✓",late="geç tespit!",hidden="görünmüyor",
 df_b=["• Alçak uçtuğu için radar ufkunun altında kalır","• Sürekli manevra → yörünge tahmin edilemez","• Tespitten çarpmaya kadar sadece birkaç dakika"],
 end_h="ÖZET",end=["Hipersonik = Mach 5'ten hızlı (>6.000 km/sa)","HGV: roketle yükselir, atmosferde süzülerek manevra yapar","Scramjet: süpersonik hava akışında yakıt yakan motor","En büyük zorluk: 2.000 °C+ ısı ve malzeme","Avantajı: hız + manevra = savunması çok zor"],
 thanks="İzlediğiniz için teşekkürler"),
'en':dict(
 title="HYPERSONIC MISSILES",tsub="How does a missile faster than 5× the speed of sound work?",tsmall="A short explainer",
 mach_h="What is Mach 5?",mach_s="Mach 1 = speed of sound ≈ 1,235 km/h (at sea level)",
 rows=[("Airliner","Mach 0.85  ~900 km/h"),("Concorde","Mach 2  ~2,180 km/h"),("Rifle bullet","Mach 2.5–3"),("Hypersonic missile","Mach 5+  >6,000 km/h")],
 mach_b="~1.7 km per second → London to Paris (~340 km) in about 3.5 minutes!",
 hgv_h="Type 1: Hypersonic Glide Vehicle (HGV)",hgv_s="Launched by a rocket, then glides without an engine",
 atm="edge of the atmosphere (~100 km)",bal="Ballistic missile: high, predictable arc",
 hgv_steps=["1) A rocket booster carries the vehicle very high and very fast","2) The glide vehicle separates, the booster falls away","3) It glides through the upper atmosphere at Mach 5–20, skipping and maneuvering"],
 hgv_ex="Examples: Avangard (Russia), DF-17 (China)",
 sc_h="Type 2: Scramjet-Powered Cruise Missile",sc_s="Supersonic Combustion Ramjet — burning fuel in supersonic airflow",
 sc_l=[("INLET","Shock waves compress","the air (no moving parts)"),("COMBUSTOR","Fuel burns in","supersonic airflow"),("NOZZLE","Expanding hot gas","produces thrust")],
 sc_b="A scramjet only works above ~Mach 4 → a rocket accelerates it first",sc_ex="Examples: Zircon (Russia), X-51A Waverider (US test vehicle)",
 ht_h="The biggest enemy: HEAT",ht_s="Slicing through air at this speed heats the surface intensely",thou=",",
 ht_b=["• Air compression and friction heat the skin above 2,000 °C","• A plasma layer forms around it → radio communication is disrupted","• Solution: carbon-carbon composites, ceramic heat shields","• Guidance: inertial navigation + satellites + advanced sensors"],
 df_h="Why is it so hard to stop?",df_s="Speed + low altitude + maneuvering = very short reaction time",radar="Radar",rh="radar line of sight",
 early="detected early ✓",late="detected late!",hidden="invisible",
 df_b=["• Flies low, staying below the radar horizon","• Constant maneuvering → unpredictable path","• Only a few minutes from detection to impact"],
 end_h="SUMMARY",end=["Hypersonic = faster than Mach 5 (>6,000 km/h)","HGV: boosted by a rocket, glides and maneuvers in the atmosphere","Scramjet: an engine burning fuel in supersonic airflow","Biggest challenge: 2,000 °C+ heat and materials","Advantage: speed + maneuvering = very hard to defend against"],
 thanks="Thanks for watching")}[LANG]
NAR={'tr':[
 ["Hipersonik füzeler.","Ses hızının beş katından hızlı giden bir füze nasıl çalışır? Birlikte bakalım."],
 ["Mak bir, ses hızıdır. Deniz seviyesinde saatte yaklaşık bin iki yüz otuz beş kilometre.","Bir yolcu uçağı Mak sıfır virgül sekiz beş ile, Konkord ise Mak iki ile uçar.","Hipersonik füzeler ise Mak beşin, yani saatte altı bin kilometrenin üzerine çıkar.","Bu hızla İstanbul ile Ankara arası yalnızca üç buçuk dakika sürer."],
 ["Birinci tür, hipersonik süzülme aracıdır.","Önce bir roket, aracı çok yükseğe ve çok hızlı çıkarır.","Ardından süzülme aracı roketten ayrılır.","Atmosferin üst katmanında, Mak beş ile yirmi arasında bir hızla süzülür ve manevra yapar.","Balistik füzelerin aksine, yörüngesi tahmin edilemez."],
 ["İkinci tür, skramjet motorlu seyir füzeleridir.","Giriş bölümü, havayı şok dalgalarıyla sıkıştırır. Motorda hareketli parça yoktur.","Yanma odasında yakıt, süpersonik hızla akan havanın içinde yakılır.","Genleşen sıcak gazlar lüleden çıkarak itki üretir.","Bu motor ancak Mak dört civarında çalıştığı için, füze önce bir roketle hızlandırılır."],
 ["Hipersonik füzelerin en büyük düşmanı ısıdır.","Havanın sıkışması ve sürtünme, yüzeyi iki bin derecenin üzerine ısıtır.","Füzenin çevresinde plazma oluşur ve bu, radyo iletişimini zorlaştırır.","Bu yüzden karbon karbon kompozitler ve seramik ısı kalkanları kullanılır."],
 ["Peki neden durdurmak bu kadar zor?","Balistik bir füze yükseğe çıktığı için radar onu erkenden görür.","Hipersonik füze ise alçaktan uçar ve radar ufkunun altında kalır.","Sürekli manevra yaptığı için yörüngesi tahmin edilemez.","Tespit ile çarpma arasında yalnızca birkaç dakika kalır."],
 ["Özetle, hipersonik füzeler yüksek hızı ve manevra yeteneğini birleştirerek savunmayı çok zorlaştırır.","İzlediğiniz için teşekkürler."]],
'en':[
 ["Hypersonic missiles.","How does a missile that flies more than five times the speed of sound actually work? Let's take a look."],
 ["Mach one is the speed of sound: about twelve hundred thirty five kilometers per hour at sea level.","An airliner cruises at Mach zero point eight five, and Concorde flew at Mach two.","Hypersonic missiles go beyond Mach five, that is, more than six thousand kilometers per hour.","At that speed, London to Paris would take only about three and a half minutes."],
 ["The first type is the hypersonic glide vehicle.","First, a rocket booster carries the vehicle very high and very fast.","Then the glide vehicle separates from the rocket.","It glides through the upper atmosphere at Mach five to twenty, skipping and maneuvering as it goes.","Unlike a ballistic missile, its path is hard to predict."],
 ["The second type is the scramjet powered cruise missile.","The inlet compresses incoming air using shock waves. There are no moving parts.","In the combustor, fuel is burned inside air that is still flowing at supersonic speed.","The expanding hot gas exits through the nozzle and produces thrust.","Because a scramjet only works above about Mach four, the missile is first accelerated by a rocket."],
 ["The biggest enemy of a hypersonic missile is heat.","Air compression and friction heat the surface to more than two thousand degrees Celsius.","A layer of plasma forms around the missile, which disrupts radio communication.","That's why engineers use carbon carbon composites and ceramic heat shields."],
 ["So why are they so hard to stop?","A ballistic missile climbs high, so radar can see it early.","A hypersonic missile flies low, staying below the radar horizon.","It keeps maneuvering, so its path can't be predicted.","Only a few minutes remain between detection and impact."],
 ["In short, hypersonic missiles combine extreme speed with maneuverability, making them very hard to defend against.","Thanks for watching."]]}[LANG]
VOICE={'tr':VD+"/tr_TR-dfki-medium.onnx",'en':VD+"/en_US-ryan-high.onnx"}[LANG]
sr=22050 if LANG=='tr' else 22050
def tts(s,i):
    fn=f"{OUT}/_n{LANG}{i}.wav"; subprocess.run(["piper","-m",VOICE,"-f",fn,"--length_scale","1.05" if LANG=='tr' else "1.0"],input=s.encode(),capture_output=True,check=True)
    w=wave.open(fn); r=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768; os.remove(fn); return a,r
segs=[]; k=0; durs=[]
BASE=[7,13,15,15,13,13,9]
for si,sents in enumerate(NAR):
    t=0.7; L=[]
    for s in sents:
        a,r=tts(s,k); k+=1; sr=r; L.append((t,a,s)); t+=len(a)/r+0.35
    durs.append(max(BASE[si],t+1.0)); segs.append(L)
W_,H_=W,H
random.seed(3)
yy=np.linspace(0,1,H)[:,None]; bg=np.zeros((H,W,3),np.uint8)
bg[...,0]=(8+10*yy); bg[...,1]=(14+18*yy); bg[...,2]=(30+30*yy)
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
    dr.polygon([(x+sc*(px*ca-py*sa),y+sc*(px*sa+py*ca)) for px,py in pts],fill=col(c,a))
def glow(dr,x,y,r,c,a=1):
    for i in range(6,0,-1):
        rr=r*i/6; dr.ellipse((x-rr,y-rr,x+rr,y+rr),fill=col(c,a*0.12))
def header(dr,t,s,sub=None):
    a=fade(t,0); text(dr,(60,50),s,fH,CY,a); dr.rectangle((60,104,60+int(220*a),108),fill=col(CY,a))
    if sub: text(dr,(60,120),sub,fS,GR,fade(t,0.3))
# scene timings scaled: cue times from narration sentence starts
def cue(si,j,default): 
    L=segs[si]; return L[j][0] if j<len(L) else default
def s_title(dr,t,D):
    p=ease(t/5); x=-100+p*(W+250); y=430-120*p
    for i in range(40):
        q=i/40; dr.line((x-q*600,y+q*600*120/1350, x-(q+0.03)*600,y+(q+0.03)*600*120/1350),fill=col(OR,0.6*(1-q)),width=int(10*(1-q))+1)
    glow(dr,x+30,y-3,40,OR,0.9); missile(dr,x,y,math.atan2(-120,1350),1.6)
    text(dr,(W/2,250),TX['title'],fT,WH,fade(t,0.8),"mm"); text(dr,(W/2,320),TX['tsub'],fM,CY,fade(t,1.6),"mm")
    text(dr,(W/2,660),TX['tsmall'],fS,GR,fade(t,2.4),"mm")
def s_mach(dr,t,D):
    header(dr,t,TX['mach_h'],TX['mach_s']); c1=cue(1,1,2)
    for i,((n,v),m,c) in enumerate(zip(TX['rows'],[0.85,2.0,2.8,5.0],[GR,BL,(170,140,255),OR])):
        st=c1+i*0.9 if i<3 else cue(1,2,c1+3); y=200+i*85; a=fade(t,st); g=ease((t-st)/1.5)
        text(dr,(60,y+10),n,fM,WH,a); dr.rectangle((330,y,330+int(m/6*780*g),y+46),fill=col(c,a))
        text(dr,(340+int(m/6*780*g),y+10),v if g>0.95 else "",fS,WH,a)
    for k in range(1,7):
        xx=330+int(780*k/6); dr.line((xx,190,xx,540),fill=col(GR,0.25*fade(t,0.5)),width=1); text(dr,(xx,555),f"M{k}",fX,GR,fade(t,0.5),"mm")
    text(dr,(W/2,630),TX['mach_b'],fM,CY,fade(t,cue(1,3,8)),"mm")
GROUND=600
def s_hgv(dr,t,D):
    header(dr,t,TX['hgv_h'],TX['hgv_s'])
    dr.rectangle((0,GROUND,W,H),fill=(20,30,40)); dr.line((0,GROUND,W,GROUND),fill=GR,width=2)
    dr.line((0,300,W,300),fill=col(BL,0.3),width=1); text(dr,(W-20,290),TX['atm'],fX,BL,0.6,"rs")
    tb=cue(2,4,10)
    if t>tb:
        pts=[(100+i*10, GROUND-380*math.sin(math.pi*i/110)) for i in range(111)]; a=fade(t,tb)
        for i in range(0,110,2): dr.line(pts[i]+pts[i+1],fill=col(GR,0.6*a),width=2)
        text(dr,(650,205),TX['bal'],fS,GR,a,"mm")
    c1,c2,c3=cue(2,1,1),cue(2,2,4),cue(2,3,6)
    def path(u):
        if u<0.25: v=u/0.25; return 100+80*v, GROUND-330*ease(v)**0.8
        v=(u-0.25)/0.75; x=180+v*1000; y=GROUND-330+v*170+28*math.sin(v*14)*(1-v)
        if v>0.85: y+=(v-0.85)/0.15*120
        return x,y
    u=0.25*cl((t-c1)/(c2-c1)) if t<c2 else 0.25+0.75*cl((t-c2)/(tb+1-c2))
    if t>c1:
        pts=[path(k/200*u) for k in range(201)]
        for i in range(200): dr.line(pts[i]+pts[i+1],fill=col(OR if i/200*u>0.25 else CY,0.85),width=3)
        x,y=pts[-1]; x2,y2=path(min(1,u+0.005)); ang=math.atan2(y2-y,x2-x)
        if u<1:
            if u<0.25: missile(dr,x,y,ang,1.4); glow(dr,x-40*math.cos(ang),y-40*math.sin(ang),25,OR)
            else:
                glow(dr,x,y,30,OR,0.8); ca,sa=math.cos(ang),math.sin(ang)
                dr.polygon([(x+22*ca,y+22*sa),(x-18*ca-9*sa,y-18*sa+9*ca),(x-18*ca+9*sa,y-18*sa-9*ca)],fill=WH)
    if c2<t<c2+2.8: bx,by=path(0.25); missile(dr,bx-10,by+(t-c2)*120,math.pi/2,1.1,(130,130,140),cl(1-(t-c2)/2.8))
    for i,s in enumerate(TX['hgv_steps']): text(dr,(60,615+i*32),s,fS,WH,fade(t,[c1,c2,c3][i]))
    text(dr,(W-30,140),TX['hgv_ex'],fS,GR,fade(t,tb+1),"rm")
def s_scram(dr,t,D):
    header(dr,t,TX['sc_h'],TX['sc_s']); oy=400
    up=[(150,oy-140),(1150,oy-140),(1150,oy-100),(1000,oy-70),(800,oy-55),(450,oy-55),(150,oy-120)]
    lo=[(250,oy+120),(450,oy+55),(800,oy+55),(1000,oy+80),(1150,oy+120),(1150,oy+140),(300,oy+140)]
    a=fade(t,0.3); dr.polygon(up,fill=col((70,80,100),a)); dr.polygon(lo,fill=col((70,80,100),a))
    dr.rectangle((800,oy-55,1000,oy-48),fill=col(OR,a*0.6))
    for fx in range(820,990,40): dr.ellipse((fx-4,oy-50,fx+4,oy-42),fill=col(CY,a))
    random.seed(1)
    for k in range(260):
        ph=random.random(); ly=random.uniform(-1,1); sp=random.uniform(0.8,1.2)
        q=(ph+t*0.25*sp)%1; x=60+q*1180
        if x<450: half=150-(x-60)/390*95
        elif x<1000: half=55+(x-800)/200*20 if x>800 else 55
        else: half=75+(x-1000)/150*55
        y=oy+ly*(half-6); c=BL if x<800 else (OR if x<1000 else RD); Ln=14 if x<800 else 18
        dr.line((x-Ln,y,x,y),fill=col(c,0.8*a),width=2)
    for (h,l1,l2),x,c,s in zip(TX['sc_l'],[300,830,1130],[BL,OR,RD],[cue(3,1,1.5),cue(3,2,4),cue(3,3,6.5)]):
        aa=fade(t,s); text(dr,(x,200),h,fM,c,aa,"mm"); text(dr,(x,560),l1,fS,WH,aa,"mm"); text(dr,(x,588),l2,fS,WH,aa,"mm")
    text(dr,(W/2,655),TX['sc_b'],fS,CY,fade(t,cue(3,4,9)),"mm"); text(dr,(W/2,688),TX['sc_ex'],fX,GR,fade(t,cue(3,4,9)+1.5),"mm")
def s_heat(dr,t,D):
    header(dr,t,TX['ht_h'],TX['ht_s']); cx,cy=430,400; g=ease((t-0.5)/6)
    for i in range(10,0,-1):
        c=(255,int(80+140*(1-i/10)),int(40*(1-i/10)))
        dr.polygon([(cx+260,cy),(cx-200,cy-30-i*14*g),(cx-200,cy+30+i*14*g)],fill=col(c,0.06+0.05*g))
    glow(dr,cx+230,cy,60+60*g,(255,190,90),0.9*g); missile(dr,cx,cy,0,5.5,(200,205,215))
    temp=int(20+2180*g); tc=(255,int(255-170*g),int(255-220*g))
    text(dr,(cx,cy+170),f"{temp:,} °C".replace(",",TX['thou']),fT,tc,fade(t,0.5),"mm")
    cs=[cue(4,1,2),cue(4,2,4),cue(4,3,6),cue(4,3,6)+2.5]
    for i,s in enumerate(TX['ht_b']):
        for j,ln in enumerate(textwrap.wrap(s,36)): text(dr,(780,200+i*110+j*30),ln,fS,WH,fade(t,cs[i]))
def s_def(dr,t,D):
    header(dr,t,TX['df_h'],TX['df_s'])
    R=3000; ex,ey=W/2,GROUND+R-40; dr.ellipse((ex-R,ey-R,ex+R,ey+R),fill=(20,34,44),outline=GR)
    rx,ry=1130,GROUND-60
    dr.polygon([(rx-20,ry+8),(rx+20,ry+8),(rx,ry-20)],fill=WH); text(dr,(rx,ry+34),TX['radar'],fX,WH,1,"mm")
    a=fade(t,0.5); dr.line((rx,ry-20,150,ry-170),fill=col(BL,0.5*a),width=2); text(dr,(300,ry-195),TX['rh'],fX,BL,a,"mm")
    t0=cue(5,1,1); u=cl((t-t0)/(D-t0-1.5))
    bp=[(80+i*9,GROUND-60-300*math.sin(math.pi*i/110)) for i in range(int(110*u)+1)]
    hp=[(80+i*9,GROUND-110-40*math.sin(i/9)*(1-i/110)) for i in range(int(110*u)+1)]
    if t>t0:
        for i in range(len(bp)-1): dr.line(bp[i]+bp[i+1],fill=col(GR,0.8),width=3)
        for i in range(len(hp)-1): dr.line(hp[i]+hp[i+1],fill=col(OR,0.95),width=3)
        glow(dr,*bp[-1],12,WH,0.7)
        if bp[-1][1]<ry-20-(rx-bp[-1][0])*150/980: text(dr,(bp[-1][0],bp[-1][1]-25),TX['early'],fX,(120,230,140),1,"mm")
        glow(dr,*hp[-1],16,OR,0.9); lim=ry-20-(rx-hp[-1][0])*150/(rx-150)
        text(dr,(hp[-1][0],hp[-1][1]+28),TX['late'] if hp[-1][1]<lim else TX['hidden'],fX,RD,1,"mm")
    for i,s in enumerate(TX['df_b']): text(dr,(60,162+i*30),s,fS,WH,fade(t,cue(5,i+2,4+i*2)))
def s_end(dr,t,D):
    text(dr,(W/2,140),TX['end_h'],fH,CY,fade(t,0),"mm")
    for i,s in enumerate(TX['end']): text(dr,(W/2,230+i*60),s,fM,WH,fade(t,0.6+i*0.7),"mm")
    text(dr,(W/2,640),TX['thanks'],fS,GR,fade(t,cue(6,1,5)),"mm")
scenes=list(zip([s_title,s_mach,s_hgv,s_scram,s_heat,s_def,s_end],durs))
total=sum(durs); starts=np.cumsum([0]+durs)
SR=44100; n=int(total*SR)+SR; tt=np.arange(n)/SR
mus=0.12*np.sin(2*np.pi*55*tt)+0.08*np.sin(2*np.pi*82.4*tt+np.sin(tt*0.3))+0.05*np.sin(2*np.pi*110*tt)
mus*=0.6+0.4*np.sin(2*np.pi*tt/8)**2
noise=np.random.default_rng(0).normal(0,1,n); mus+=np.exp(-((tt-2.5)/1.2)**2)*np.convolve(noise,np.ones(40)/40,'same')*0.6
voice=np.zeros(n); srt=[]; idx=1
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:02}:{m:02}:{int(s):02},{int((s%1)*1000):03}"
for si,L in enumerate(segs):
    for (t0,a,s) in L:
        st=starts[si]+t0; up=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a)
        i0=int(st*SR); voice[i0:i0+len(up)]+=up[:n-i0]
        srt.append(f"{idx}\n{ts(st)} --> {ts(st+len(a)/sr)}\n{s.replace('Mak ','Mach ').replace('skramjet','scramjet').replace('Konkord','Concorde')}\n"); idx+=1
duck=np.convolve((np.abs(voice)>0.01).astype(float),np.ones(SR//2)/(SR//2),'same')
aud=mus*(1-0.65*np.clip(duck*3,0,1))*0.8+voice*0.95
aud*=np.minimum(1,np.minimum(tt/1.5,np.maximum(0,(total-tt)/2.5)))
aud=aud/max(1,np.abs(aud).max()/0.95)
wf=f"{OUT}/_a{LANG}.wav"
with wave.open(wf,"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((aud*32000).astype(np.int16).tobytes())
open(f"{OUT}/hypersonic-{LANG}.srt","w").write("\n".join(srt))
mp4=f"{OUT}/"+("hipersonik-fuzeler-tr.mp4" if LANG=='tr' else "hypersonic-missiles-en.mp4")
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wf,
 "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",mp4],stdin=subprocess.PIPE)
for fn,D in scenes:
    for k in range(int(D*FPS)):
        t=k/FPS; img=BG.copy(); dr=ImageDraw.Draw(img,"RGBA"); fn(dr,t,D)
        f=min(1,t/0.5,(D-t)/0.5)
        if f<1: dr.rectangle((0,0,W,H),fill=(0,0,0,int(255*(1-f))))
        p.stdin.write(img.tobytes())
p.stdin.close(); p.wait(); os.remove(wf)
# thumbnail
img=BG.copy(); dr=ImageDraw.Draw(img,"RGBA"); s_title(dr,3.0,7); img.save(f"{OUT}/thumbnail-{LANG}.png")
print(mp4,round(total,1),[round(d,1) for d in durs])
