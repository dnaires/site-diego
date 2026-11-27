"""Troca o fundo carmim do fim da abertura por vinho escuro, sem tocar no ícone oficial (26/11).
O ícone oficial (assets/logo/icone.webp) é opaco e o vermelho dele (#9F2638) é quase o carmim do fundo
(#9D2235): no último quadro o símbolo se confundia com o fundo. Este script pega cada quadro da onda
(340 a 396), estima quanto de carmim é fundo (projeção na reta preto -> carmim) e troca só essa parte
pela cor nova; a área do ícone (alpha do icone.webp na posição 58,299, 973x1358) fica intacta.
Uso (da pasta Site Diego): extraia os quadros 340-396 de referencias/abertura_completa_v2.mp4 em PNG,
rode recolor(F, fundo('#3a0b14')) em cada um, junte com os quadros 0-339 (crf 10) e rode codificar_scroll.py.
Resultado de 26/11: referencias/abertura_completa_v3.mp4."""
import sys, numpy as np
from PIL import Image, ImageFilter
C=np.array([0x9a,0x21,0x33],float)
ic=Image.open('assets/logo/icone.webp').convert('RGBA').resize((973,1358),Image.LANCZOS)
A=Image.new('L',(1080,1920),0); A.paste(ic.split()[3],(58,299))
Aa=np.array(A)/255.
yy,xx=np.mgrid[0:1920,0:1080].astype(float)
def fundo(modo):
    if modo.startswith('#'):
        c=np.array([int(modo[i:i+2],16) for i in (1,3,5)],float); return np.broadcast_to(c,(1920,1080,3))
    # halo: escuro no centro do ícone, carmim nas bordas
    escuro=np.array([0x3a,0x0b,0x14],float)
    r=np.sqrt(((xx-544)/700)**2+((yy-977)/1000)**2)
    k=np.clip((r-0.35)/0.65,0,1); k=k*k*(3-2*k)
    return escuro*(1-k[...,None])+C*k[...,None]
def recolor(F,G):
    w=np.clip((F@C)/(C@C),0,1)
    res=np.linalg.norm(F-w[...,None]*C,axis=2)
    key=np.clip((res-8)/22,0,1)
    m=np.maximum(Aa,key)
    out=F+((1-m)*w)[...,None]*(G-C)
    return np.clip(out+np.random.uniform(-.5,.5,out.shape),0,255).astype(np.uint8)
