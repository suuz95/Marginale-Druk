# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 18:49:47 2023

@author: Suzanne

Bronnen:
    
https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/inkomstenbelasting/heffingskortingen_boxen_tarieven/boxen_en_tarieven/overzicht_tarieven_en_schijven/u-hebt-in-2023-nog-niet-aow-leeftijd

https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/inkomstenbelasting/heffingskortingen_boxen_tarieven/heffingskortingen/arbeidskorting/tabel-arbeidskorting-2023

https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/inkomstenbelasting/heffingskortingen_boxen_tarieven/heffingskortingen/algemene_heffingskorting/tabel-algemene-heffingskorting-2023

https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/inkomstenbelasting/heffingskortingen_boxen_tarieven/heffingskortingen/inkomensafhankelijke_combikorting/inkomensafhankelijke_combinatiekorting

https://download.belastingdienst.nl/toeslagen/docs/berekening_zorgtoeslag_tg0821z32fd.pdf

https://download.belastingdienst.nl/toeslagen/docs/berekening_huurtoeslag_tg0831z32fd.pdf

https://download.belastingdienst.nl/toeslagen/docs/berekening_kindgebonden_budget_tg0811z32fd.pdf

https://download.belastingdienst.nl/toeslagen/docs/berekening_kinderopvangtoeslag_tg0801z32fd.pdf
"""

#Todo: 
#-Inkomstenbelasting & heffingskortingen AOW meenemen
#-Afbetaling studielening meenemen
#-HRA meenemen


import numpy as np
import matplotlib.pyplot as plt

def Inkomsten_belasting(Inkomen):
    Grens_schijf1=73031
    Tarief_schijf1=36.93
    Tarief_schijf2=49.50
    
    Belasting=Inkomen*Tarief_schijf1/100+np.clip(Inkomen-Grens_schijf1,0,None)*(Tarief_schijf2-Tarief_schijf1)/100
    return Belasting

def Algemene_heffinskorting(Inkomen):
    Algemene_heffinskorting_basis=3070
    Afbouw_algemene_heffinskorting=22661
    Percentage_afbouw_algemene_heffingskorting=6.095
    
    if type(Inkomen)==int:
        Inkomen=np.array([Inkomen])
    
    Algemene_heffinskorting=Algemene_heffinskorting_basis-(Inkomen-Afbouw_algemene_heffinskorting)*Percentage_afbouw_algemene_heffingskorting/100
    Algemene_heffinskorting[np.where(Algemene_heffinskorting>Algemene_heffinskorting_basis)]=Algemene_heffinskorting_basis
    Algemene_heffinskorting[np.where(Algemene_heffinskorting<0)]=0
    return Algemene_heffinskorting

def Arbeidskorting(Inkomen):
    Arbeidskorting=np.zeros(np.size(Inkomen))
    Arbeidskorting_grenzen=np.array([10741,23201,37691,115295])
    Arbeidskorting_percentages=np.array([8.231,29.861,3.085,-6.510])
    Convert_back=False
    if type(Inkomen)==int:
        Inkomen=np.array([Inkomen])
        Convert_back=True
        
    Arbeidskorting[np.where(Inkomen<Arbeidskorting_grenzen[0])]=Arbeidskorting_percentages[0]/100*Inkomen[np.where(Inkomen<Arbeidskorting_grenzen[0])]
    Arbeidskorting[np.where((Inkomen<=Arbeidskorting_grenzen[1]) & (Inkomen>Arbeidskorting_grenzen[0]))]=Arbeidskorting_percentages[0]/100*Arbeidskorting_grenzen[0]+(Inkomen[np.where((Inkomen<Arbeidskorting_grenzen[1]) & (Inkomen>Arbeidskorting_grenzen[0]))]-Arbeidskorting_grenzen[0])*Arbeidskorting_percentages[1]/100
    Arbeidskorting[np.where((Inkomen<=Arbeidskorting_grenzen[2]) & (Inkomen>Arbeidskorting_grenzen[1]))]=Arbeidskorting_percentages[0]/100*Arbeidskorting_grenzen[0]+(Arbeidskorting_grenzen[1]-Arbeidskorting_grenzen[0])*Arbeidskorting_percentages[1]/100+(Inkomen[np.where((Inkomen<Arbeidskorting_grenzen[2]) & (Inkomen>Arbeidskorting_grenzen[1]))]-Arbeidskorting_grenzen[1])*Arbeidskorting_percentages[2]/100
    Arbeidskorting[np.where((Inkomen<=Arbeidskorting_grenzen[3]) & (Inkomen>Arbeidskorting_grenzen[2]))]=Arbeidskorting_percentages[0]/100*Arbeidskorting_grenzen[0]+(Arbeidskorting_grenzen[1]-Arbeidskorting_grenzen[0])*Arbeidskorting_percentages[1]/100+(Arbeidskorting_grenzen[2]-Arbeidskorting_grenzen[1])*Arbeidskorting_percentages[2]/100+(Inkomen[np.where((Inkomen<Arbeidskorting_grenzen[3]) & (Inkomen>Arbeidskorting_grenzen[2]))]-Arbeidskorting_grenzen[2])*Arbeidskorting_percentages[3]/100
    
    if Convert_back:
        return int(Arbeidskorting)
    else:
        return Arbeidskorting
def Inkomensafhankelijke_combinatiekorting(Inkomen,Kinderen_onder_12):
    ICAK_grenzen=[5548,29076]
    ICAK_percentage=11.45
    ICAK=np.zeros(np.size(Inkomen))
    Convert_back=False
    if type(Inkomen)==int:
        Inkomen=np.array([Inkomen])
        Convert_back=True
    if Kinderen_onder_12>0: 
        ICAK[np.where(Inkomen<ICAK_grenzen[0])]=0
        ICAK[np.where((Inkomen<=ICAK_grenzen[1]) & (Inkomen>ICAK_grenzen[0]))]=(Inkomen[np.where((Inkomen<=ICAK_grenzen[1]) & (Inkomen>ICAK_grenzen[0]))]-ICAK_grenzen[0])*ICAK_percentage/100
        ICAK[np.where(Inkomen>ICAK_grenzen[1])]=(ICAK_grenzen[1]-ICAK_grenzen[0])*ICAK_percentage/100
        
    if Convert_back:
        return int(ICAK)
    else:
        return ICAK
    

def Zorgtoeslag(Inkomen_samen,Mensen_in_huis=1):
    drempelinkomen=25070

    Standaardpremie=1889
    normpremie_alleen=np.clip(0.123/100*drempelinkomen+13.64/100*(Inkomen_samen-drempelinkomen),0.123/100*drempelinkomen,Standaardpremie)
    normpremie_samen=np.clip(2.378/100*drempelinkomen+13.64/100*(Inkomen_samen-drempelinkomen),2.378/100*drempelinkomen,Standaardpremie*2)
    if Mensen_in_huis==1:
        Zorgtoeslag=Standaardpremie-normpremie_alleen
    else:
        Zorgtoeslag=Standaardpremie*2-normpremie_samen
    return Zorgtoeslag

def Huurtoeslag(Inkomen_samen,Huur,Mensen_in_huis=1,AOW=False,Onder_21=False):
    
    if Onder_21:
        Huurgrens=452.20
    else:
        Huurgrens=808.06
        
    Factor_a=np.array([0.000000474433,0.000000279402,0.000000671404,0.000000430722])
    Factor_b=np.array([0.002448638402, 0.001893212113, -0.002850602044, -0.003611907743])
    Kwaliteitskortingsgrens=452.20
    Taakstelling=0
    Minimum_basishuur=[225.54,225.54,223.72,221.91]
    if Mensen_in_huis==1:
        if AOW:
            Basishuur=np.clip((Factor_a[2]*Inkomen_samen**2)+(Factor_b[2]*Inkomen_samen)+Taakstelling,Minimum_basishuur[2],None)
        else:
            Basishuur=np.clip((Factor_a[0]*Inkomen_samen**2)+(Factor_b[0]*Inkomen_samen)+Taakstelling,Minimum_basishuur[0],None)  
    else:
        if AOW:
            Basishuur=np.clip((Factor_a[3]*Inkomen_samen**2)+(Factor_b[3]*Inkomen_samen)+Taakstelling,Minimum_basishuur[3],None)
        else:
            Basishuur=np.clip((Factor_a[1]*Inkomen_samen**2)+(Factor_b[1]*Inkomen_samen)+Taakstelling,Minimum_basishuur[1],None)
    if Mensen_in_huis<=2:
        Aftopgrens=647.19
    else:
        Aftopgrens=693.60
        
    if Huur<=Kwaliteitskortingsgrens:
        Huurtoeslag=np.clip(Huur-Basishuur,0,None)
    elif Huur<=Aftopgrens:
        Huurtoeslag=np.clip(Kwaliteitskortingsgrens-Basishuur,0,None)+np.clip(0.65*(Huur-Basishuur),0,0.65*(Huur-Kwaliteitskortingsgrens))
    elif Huur<=Huurgrens:
        Huurtoeslag=np.clip(Kwaliteitskortingsgrens-Basishuur,0,None)+np.clip(0.65*(Aftopgrens-Basishuur),0,0.65*(Aftopgrens-Kwaliteitskortingsgrens))
        if AOW or Mensen_in_huis==1:
            Huurtoeslag+=0.4*np.clip((Huur-Basishuur),0,(Huur-Aftopgrens))
    else:
        Huurtoeslag=np.zeros(len(Inkomen_samen))
    Huurtoeslag*=12
    return Huurtoeslag

def Kindgebonden_budget(Inkomen_samen,Volwassenen=1,Kinderen=1,Kinderen_12_15=0,Kinderen_16_17=0):
    if Volwassenen==1:
        Max_inkomen_kind_budget=25070
        if Kinderen==1:
            Max_kind_budget=5501
        else:
            Max_kind_budget=7033+(Kinderen-2)*1532
    else:
        Max_inkomen_kind_budget=43397
        if Kinderen==1:
            Max_kind_budget=1653
        else:
            Max_kind_budget=3185+(Kinderen-2)*1532

    Max_kind_budget+=267*Kinderen_12_15+476*Kinderen_16_17        
        
    Kindgebonden_budget=np.clip(Max_kind_budget-0.0675*(Inkomen_samen-Max_inkomen_kind_budget),0,Max_kind_budget)
    return Kindgebonden_budget

def Kinderopvangtoeslag(Inkomen_samen,Uren_per_maand,Uurtarief=9,Opvang='KDV',Eerste_kind=True):
    if Opvang=='KDV':
        Max_uur_vergoeding=9.12
    elif Opvang=='BSO':
        Max_uur_vergoeding=7.85
    elif Opvang=='Gast':
        Max_uur_vergoeding=6.85
    else:
        print('Geen opvang gekozen')
    
    if Uurtarief<Max_uur_vergoeding:
        Max_uur_vergoeding=Uurtarief
    Max_Uren_maand=230
    
    Uren_vergoed=np.clip(Uren_per_maand,0,Max_Uren_maand)
    
    Tabel_toeslag=np.array([[0.00,21278.00,96.00,96.00],
    [21279.00,22695.00,96.00,96.00],
    [22696.00,24110.00,96.00,96.00],
    [24111.00,25528.00,96.00,96.00],
    [25529.00,26944.00,96.00,96.00],
    [26945.00,28362.00,95.50,95.60],
    [28363.00,29778.00,94.40,95.40],
    [29779.00,31191.00,93.40,95.20],
    [31192.00,32715.00,92.50,95.00],
    [32716.00,34236.00,91.90,94.90],
    [34237.00,35762.00,90.90,94.70],
    [35763.00,37283.00,90.40,94.50],
    [37284.00,38811.00,89.50,94.50],
    [38812.00,40334.00,88.70,94.50],
    [40335.00,41894.00,88.10,94.50],
    [41895.00,43456.00,87.30,94.50],
    [43457.00,45018.00,86.60,94.50],
    [45019.00,46580.00,85.90,94.50],
    [46581.00,48145.00,85.00,94.50],
    [48146.00,49706.00,84.50,94.50],
    [49707.00,51267.00,83.70,94.50],
    [51268.00,52830.00,83.00,94.50],
    [52831.00,54537.00,82.10,94.50],
    [54538.00,57885.00,80.60,94.50],
    [57886.00,61231.00,79.80,94.10],
    [61232.00,64579.00,78.70,93.50],
    [64580.00,67929.00,76.40,93.10],
    [67930.00,71275.00,74.10,92.80],
    [71276.00,74625.00,71.90,92.10],
    [74626.00,77972.00,69.40,91.60],
    [77973.00,81320.00,67.10,91.10],
    [81321.00,84669.00,64.90,90.40],
    [84670.00,88015.00,62.50,89.80],
    [88016.00,91367.00,60.30,89.40],
    [91368.00,94714.00,57.80,89.10],
    [94715.00,98060.00,55.50,88.40],
    [98061.00,101408.00,53.30,88.00],
    [101409.00,104822.00,50.90,87.50],
    [104823.00,108252.00,48.80,86.80],
    [108253.00,111680.00,46.70,86.30],
    [111681.00,115109.00,44.60,85.90],
    [115110.00,118535.00,42.40,85.60],
    [118536.00,121965.00,40.50,84.90],
    [121966.00,125395.00,38.60,84.30],
    [125396.00,128825.00,36.70,83.90],
    [128826.00,132250.00,34.70,83.30],
    [132251.00,135678.00,33.30,82.90],
    [135679.00,139109.00,33.30,82.20],
    [139110.00,142536.00,33.30,81.60],
    [142537.00,145965.00,33.30,80.60],
    [145966.00,149392.00,33.30,80.30],
    [149393.00,152822.00,33.30,79.50],
    [152823.00,156254.00,33.30,78.60],
    [156255.00,159680.00,33.30,78.00],
    [159681.00,163109.00,33.30,77.10],
    [163110.00,166535.00,33.30,76.60],
    [166536.00,169966.00,33.30,75.80],
    [169967.00,173396.00,33.30,75.10],
    [173397.00,176824.00,33.30,74.40],
    [176825.00,180252.00,33.30,73.40],
    [180253.00,183677.00,33.30,72.90],
    [183678.00,187109.00,33.30,72.20],
    [187110.00,190536.00,33.30,71.40],
    [190537.00,193966.00,33.30,70.70],
    [193967.00,197395.00,33.30,70.10],
    [197396.00,200822.00,33.30,69.30],
    [200823.00,204252.00,33.30,68.50],
    [204253.00,207679.00,33.30,68.00],
    [207680.00,99999999.00,33.30,67.10]])
    

    #print(Tabel_toeslag[np.where(Tabel_toeslag[:,0]>Inkomen_samen)[0][0]-1,2]/100)
    if Eerste_kind:
        if Inkomen_samen>Tabel_toeslag[-1,0]:
            Vergoeding=Max_uur_vergoeding*Uren_vergoed*Tabel_toeslag[-1,2]/100*12
        else:
            
            Vergoeding=Max_uur_vergoeding*Uren_vergoed*Tabel_toeslag[np.where(Tabel_toeslag[:,0]>Inkomen_samen)[0][0]-1,2]/100*12
    else:
        if Inkomen_samen>Tabel_toeslag[-1,0]:
            Vergoeding=Max_uur_vergoeding*Uren_vergoed*Tabel_toeslag[-1,3]/100*12
        else:
            Vergoeding=Max_uur_vergoeding*Uren_vergoed*Tabel_toeslag[np.where(Tabel_toeslag[:,0]>Inkomen_samen)[0][0]-1,3]/100*12
    return Vergoeding

def Belastingschijven():
    Bruto_Inkomen=np.arange(100,130000,100,dtype='longlong')
    Betaalde_belasting=np.clip(Inkomsten_belasting(Bruto_Inkomen)-Algemene_heffinskorting(Bruto_Inkomen)-Arbeidskorting(Bruto_Inkomen),0,None)
    Netto_Inkomen=Bruto_Inkomen-Betaalde_belasting
    
    Marginaal_tarief_belasting=np.diff(Betaalde_belasting,prepend=0)/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100
    Belastingdruk=Betaalde_belasting/Bruto_Inkomen*100
    plt.figure()
    plt.plot(Bruto_Inkomen,Netto_Inkomen,label='Netto inkomen',linewidth=2)
    plt.plot(Bruto_Inkomen,Inkomsten_belasting(Bruto_Inkomen),label='IB schijf 1 + schijf 2')
    plt.plot(Bruto_Inkomen,Algemene_heffinskorting(Bruto_Inkomen),label='Algemene heffinskorting')
    plt.plot(Bruto_Inkomen,Arbeidskorting(Bruto_Inkomen),label='Arbeidskorting')
    plt.plot(Bruto_Inkomen,Betaalde_belasting,'k',label='Daadwerkelijke belasting',linewidth=2)
    plt.grid()
    plt.legend()
    plt.xlabel('Bruto inkomen (€)')
    plt.ylabel('(€)')
    
    plt.figure()
    plt.plot(Bruto_Inkomen,Marginaal_tarief_belasting,label='Totaal loonbelasting')
    plt.plot(Bruto_Inkomen,np.diff(Inkomsten_belasting(Bruto_Inkomen),prepend=0)/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100,label='IB schijf 1 + schijf 2',color='brown')
    plt.plot(Bruto_Inkomen,-np.diff(Algemene_heffinskorting(Bruto_Inkomen),prepend=3048)/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100,label='Algemene heffinskorting',color='orange')
    plt.plot(Bruto_Inkomen,-np.diff(Arbeidskorting(Bruto_Inkomen),prepend=0)/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100,label='Arbeidskorting',color='red')
    plt.plot(Bruto_Inkomen,Belastingdruk,label='Belastingdruk',color='k',linewidth='2')
    plt.xlabel('Bruto inkomen (€)')
    plt.ylabel('Marginaal tarief (%)')
    plt.grid()
    plt.ylim([-40,110])
    plt.xlim([0,130000])
    plt.legend()

def Grafieken(Volwassenen,Kinderen_leeftijd,Huur=0,Onder_21=False,AOW=False,Opvang_kinderen='',Bruto_Inkomen_partner_1=0,Uurtarief=[9.12],Uren_per_maand=[143],title='',xlabel='Bruto Inkomen',y_label_1='(€)',y_label_2='Marginaal tarief (%)',xlim=[0,130000],ylim_1=[0,100000],ylim_2=[0,100]):
    Bruto_Inkomen=np.arange(100,130000,100,dtype='longlong')
    Kinderen=len(Kinderen_leeftijd)
    
    Betaalde_inkomsten_belasting=np.clip(Inkomsten_belasting(Bruto_Inkomen)-Algemene_heffinskorting(Bruto_Inkomen)-Arbeidskorting(Bruto_Inkomen),0,None)
    Netto_Inkomen=Bruto_Inkomen-Betaalde_inkomsten_belasting
   
    if Volwassenen>1:
        Netto_Inkomen_partner_1=Bruto_Inkomen_partner_1-np.clip(Inkomsten_belasting(Bruto_Inkomen_partner_1)-Algemene_heffinskorting(Bruto_Inkomen_partner_1)-Arbeidskorting(Bruto_Inkomen_partner_1),0,None)

        Netto_Inkomen_samen=Netto_Inkomen+Netto_Inkomen_partner_1
        Bruto_Inkomen_samen=Bruto_Inkomen+Bruto_Inkomen_partner_1
        if Kinderen>0:
            if (np.count_nonzero(Kinderen_leeftijd<12)>0) & Kinderen>0:
                ICAK=np.zeros(len(Bruto_Inkomen))
                ICAK[np.where(Bruto_Inkomen<Bruto_Inkomen_partner_1)]=Inkomensafhankelijke_combinatiekorting(Bruto_Inkomen[np.where(Bruto_Inkomen<Bruto_Inkomen_partner_1)],np.count_nonzero(Kinderen<12))
                ICAK[np.where(Bruto_Inkomen>=Bruto_Inkomen_partner_1)]=Inkomensafhankelijke_combinatiekorting(Bruto_Inkomen_partner_1,np.count_nonzero(Kinderen<12))       
                Netto_Inkomen_samen+=ICAK
                Betaalde_inkomsten_belasting-=ICAK
            else:
                ICAK=np.zeros(len(Bruto_Inkomen))
    else:
        Netto_Inkomen_samen=Netto_Inkomen
        Netto_Inkomen_partner_1=0
        Bruto_Inkomen_samen=Bruto_Inkomen
        if Kinderen>0:
            if (np.count_nonzero(Kinderen_leeftijd<12)>0):
        
                ICAK=Inkomensafhankelijke_combinatiekorting(Bruto_Inkomen,np.count_nonzero(Kinderen<12))
                Netto_Inkomen_samen+=ICAK
                Betaalde_inkomsten_belasting-=ICAK
            else:
                ICAK=np.zeros(len(Bruto_Inkomen))
        
    

    
    Huurtoeslag_inkomen=Huurtoeslag(Bruto_Inkomen_samen,Huur,Volwassenen+Kinderen,AOW,Onder_21)
    Zorgtoeslag_inkomen=Zorgtoeslag(Bruto_Inkomen_samen,Volwassenen+Kinderen)
    if Kinderen>0:
        Kindgebonden_inkomen=Kindgebonden_budget(Bruto_Inkomen_samen,Volwassenen,Kinderen,np.count_nonzero(np.logical_and(Kinderen>=12, Kinderen<=15)),np.count_nonzero(np.logical_and(Kinderen>=16, Kinderen<=17)))
        if len(Opvang_kinderen)==0:
            Kinderopvangtoeslag_inkomen=0
        else:
            Kinderopvangtoeslag_inkomen=np.zeros(len(Bruto_Inkomen_samen))
          
            for i_inkomen in range(len(Kinderopvangtoeslag_inkomen)):
                for i_opvang in range(np.size(Opvang_kinderen)):
                    if Uren_per_maand[i_opvang]==max(Uren_per_maand):
                        Eerste_kind=True
                    else:
                        Eerste_kind=False
                    Kinderopvangtoeslag_inkomen[i_inkomen]+=Kinderopvangtoeslag(Bruto_Inkomen_samen[i_inkomen],Uren_per_maand[i_opvang], Uurtarief[i_opvang],Opvang=Opvang_kinderen[i_opvang],Eerste_kind=Eerste_kind)
    else:
        Kindgebonden_inkomen=0
        Kinderopvangtoeslag_inkomen=0
    Netto_Inkomen_Toeslagen_zonder_KDV=Netto_Inkomen_samen+Zorgtoeslag_inkomen+Huurtoeslag_inkomen+Kindgebonden_inkomen
    Netto_Inkomen_Toeslagen=Netto_Inkomen_Toeslagen_zonder_KDV+Kinderopvangtoeslag_inkomen
    Effectieve_belasting=Bruto_Inkomen_samen-Netto_Inkomen_Toeslagen
    plt.figure()
    plt.plot(Bruto_Inkomen,Netto_Inkomen_Toeslagen,color='blue',label='Netto+toeslagen')
    plt.plot(Bruto_Inkomen,Netto_Inkomen_samen,color='red',label='Netto inkomen')
    if np.max(Huurtoeslag_inkomen)>0:
        plt.plot(Bruto_Inkomen,Huurtoeslag_inkomen,color='green',label='Huurtoeslag')
    if np.max(Zorgtoeslag_inkomen)>0:
        plt.plot(Bruto_Inkomen,Zorgtoeslag_inkomen,color='orange',label='Zorgtoeslag')
    if np.max(Kinderopvangtoeslag_inkomen)>0:
        plt.plot(Bruto_Inkomen,Kinderopvangtoeslag_inkomen,color='purple',label='Kinderopvangtoeslag')
    if np.max(Kindgebonden_inkomen)>0:
        plt.plot(Bruto_Inkomen,Kindgebonden_inkomen,color='brown',label='Kindgebonden budget')
    
   
    plt.plot(Bruto_Inkomen,Effectieve_belasting,color='k',label='Effectieve belasting')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel('(€)')
    plt.xlim(xlim)
    plt.ylim(ylim_1)
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.title(title)
    plt.grid()
    
    
    Marginaal_KDV=np.zeros(len(Bruto_Inkomen_samen))
    if np.max(Kinderopvangtoeslag_inkomen)>0:
        
        KDV_toeslag_uniek=np.unique(Kinderopvangtoeslag_inkomen)
        Bruto_inkomen_uniek=np.zeros(len(KDV_toeslag_uniek))
        
        for i in range(len(KDV_toeslag_uniek)):
            Bruto_inkomen_uniek[i]=Bruto_Inkomen_samen[np.where(Kinderopvangtoeslag_inkomen==KDV_toeslag_uniek[i])[0][0]]
        
        
        for i in range(len(Bruto_Inkomen_samen)):
            if Bruto_Inkomen_samen[i]>min(Bruto_inkomen_uniek):
                Positie=np.where(Bruto_Inkomen_samen[i]>Bruto_inkomen_uniek)[0][0]
                Marginaal_KDV[i]=(KDV_toeslag_uniek[Positie]-KDV_toeslag_uniek[Positie-1])/(Bruto_inkomen_uniek[Positie-1]-Bruto_inkomen_uniek[Positie])*100

    Marginaal_tarief_totaal=100-(np.diff(Netto_Inkomen_Toeslagen_zonder_KDV,prepend=Netto_Inkomen_Toeslagen_zonder_KDV[0])/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100)+Marginaal_KDV

    
    
    plt.figure()
    plt.plot(Bruto_Inkomen,Marginaal_tarief_totaal,color='blue',label='Totaal marginaal tarief')
    #plt.plot(Bruto_Inkomen,np.diff(Betaalde_inkomsten_belasting,prepend=Betaalde_inkomsten_belasting[0])+np.diff(-Huurtoeslag_inkomen,prepend=Huurtoeslag_inkomen[0])+np.diff(-Zorgtoeslag_inkomen,prepend=Zorgtoeslag_inkomen[0]))
    plt.plot(Bruto_Inkomen,np.diff(Betaalde_inkomsten_belasting,prepend=Betaalde_inkomsten_belasting[0])/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100,color='red',label='Inkomstenbelasting')
    if np.max(Huurtoeslag_inkomen)>0:
        plt.plot(Bruto_Inkomen,np.diff(-Huurtoeslag_inkomen,prepend=Huurtoeslag_inkomen[0])/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100,color='green',label='Huurtoeslag')
    if np.max(Zorgtoeslag_inkomen)>0:
        plt.plot(Bruto_Inkomen,np.diff(-Zorgtoeslag_inkomen,prepend=Zorgtoeslag_inkomen[0])/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100,color='orange',label='Zorgtoeslag')
    if np.max(Kinderopvangtoeslag_inkomen)>0:        
        plt.plot(Bruto_Inkomen,Marginaal_KDV,color='purple',label='Kinderopvangtoeslag')
    if np.max(Kindgebonden_inkomen)>0:
        plt.plot(Bruto_Inkomen,np.diff(-Kindgebonden_inkomen,prepend=Kindgebonden_inkomen[0])/(Bruto_Inkomen[-1]-Bruto_Inkomen[-2])*100,color='brown',label='Kindgebonden budget')
    plt.plot(Bruto_Inkomen,Effectieve_belasting/Bruto_Inkomen_samen*100,color='k',label='Effectieve belastingdruk')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel('Marginale druk (%)')
    plt.xlim(xlim)
    plt.ylim(ylim_2)
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.title(title)
    plt.grid()
    
    
    
    
    
    
    

# #Belastinschijven
    
Belastingschijven()



# #Scenario 1

Huur=600
Volwassenen=1
Kinderen=[]
    
Grafieken(Volwassenen,Kinderen,Huur=Huur,title='Alleenstaande, Huur=600')


# #Scenario 2

Huur=800
Volwassenen=1
Kinderen=np.array([10,15])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,title='Alleenstaande ouder, Huur=800, kinderen 10 & 15')


# #Scenario 3

Huur=800
Volwassenen=1
Kinderen=np.array([2,5])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Opvang_kinderen=['KDV'],Uurtarief=[9.12],Uren_per_maand=[143],ylim_2=[0,120],title='Alleenstaande ouder, Huur=800, kinderen 2 & 5, 1x 3 dagen opvang KDV')


# #Scenario 4
Huur=800
Volwassenen=1
Kinderen=np.array([1,3])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Opvang_kinderen=['KDV','KDV'],Uurtarief=[9.12,9.12],Uren_per_maand=[143,143],ylim_2=[0,120],title='Alleenstaande ouder, Huur=800, kinderen 1&3, 2x 3 dagen opvang KDV')

# #Scenario 5
Huur=800
Volwassenen=2
Kinderen=np.array([1,3])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Opvang_kinderen=['KDV','KDV'],Uurtarief=[9.12,9.12],Uren_per_maand=[143,143],ylim_2=[0,120],title='Eenverdiener, Huur=800, kinderen 1&3, 2x 3 dagen opvang KDV')

# #Scenario 6
Huur=800
Volwassenen=2
Kinderen=np.array([10,13,17])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,title='Eenverdiener, Huur=800, kinderen 10,13 &17')


# #Scenario 7
Huur=600
Volwassenen=2
Kinderen=np.array([])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Bruto_Inkomen_partner_1=10000,title='Partner 1: 10k bruto, Huur 600, geen kinderen')


# #Scenario 8
Huur=1500
Volwassenen=2
Kinderen=np.array([])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Bruto_Inkomen_partner_1=40000,ylim_1=[0,150000],title='Partner 1: 40k bruto, geen kinderen')


# #Scenario 9
Huur=1500
Volwassenen=2
Kinderen=np.array([])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Bruto_Inkomen_partner_1=80000,ylim_1=[0,150000],title='Partner 1: 80k bruto, geen kinderen')


# #Scenario 10
Huur=600
Volwassenen=2
Kinderen=np.array([1,3])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Bruto_Inkomen_partner_1=15000,Opvang_kinderen=['KDV','KDV'],Uurtarief=[9.12,9.12],Uren_per_maand=[143,143],title='Partner 1: 15k bruto, Huur 800, 2x3 dagen opvang kinderen 1 & 3')


 # #Scenario 11
Huur=1500
Volwassenen=2
Kinderen=np.array([1,3])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Bruto_Inkomen_partner_1=40000,ylim_1=[0,150000],Opvang_kinderen=['KDV','KDV'],Uurtarief=[9.12,9.12],Uren_per_maand=[143,143],title='Partner 1: 40k bruto, 2x3 dagen opvang kinderen 1 & 3')

 # #Scenario 12
Huur=1500
Volwassenen=2
Kinderen=np.array([1,3])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Bruto_Inkomen_partner_1=80000,ylim_1=[0,150000],Opvang_kinderen=['KDV','KDV'],Uurtarief=[9.12,9.12],Uren_per_maand=[143,143],title='Partner 1: 80k bruto, 2x3 dagen opvang kinderen 1 & 3')


 # #Scenario 13
Huur=1500
Volwassenen=2
Kinderen=np.array([15,17])

    
Grafieken(Volwassenen,Kinderen,Huur=Huur,Bruto_Inkomen_partner_1=80000,ylim_1=[0,150000],title='Partner 1: 80k bruto, kinderen 15 & 17')










