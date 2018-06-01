import ROOT as rt
from array import *
from sms import *
from color import *
import CMS_lumi
class smsPlotABS(object):
    # modelname is the sms name (see sms.py)
    # histo is the 2D xsec map
    # obsLimits is a list of opbserved limits [NOMINAL, +1SIGMA, -1SIGMA]
    # expLimits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # label is a label referring to the analysis (e.g. RA1, RA2, RA2b, etc)

    def __init__(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary, label):
        self.standardDef(modelname, histo, obsLimits, expLimits, energy, lumi, preliminary)
        self.LABEL = label
        self.c = rt.TCanvas("cABS_%s" %label,"cABS_%s" %label,300,300)
        self.histo = histo

    def standardDef(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary,makeHisto=True):
        # which SMS?
        self.model = sms(modelname)
        self.OBS = obsLimits

        for bin in range(0, self.OBS['nominal'][0].GetN()):
            self.OBS['nominal'][0].SetPoint(bin,0,0)
            self.OBS['plus'][0].SetPoint(bin,0,0)
            self.OBS['minus'][0].SetPoint(bin,0,0)
       
        self.EXP = expLimits
        self.lumi = lumi
        self.energy = energy
        self.preliminary = preliminary
        # create the reference empty histo
        if makeHisto:
            self.emptyHistogramFromModel()

    def emptyHistogramFromModel(self,lims=None):
        if lims:
            self.emptyHisto = rt.TH2D("emptyHisto"+self.LABEL, "", 1, lims[0], lims[1], 
                                  1, lims[2], lims[3])
        else:
            self.emptyHisto = rt.TH2D("emptyHisto"+self.LABEL, "", 1, self.model.Xmin, self.model.Xmax, 
                                  1, self.model.Ymin, self.model.Ymax)
        
    # define the plot canvas
    def setStyle(self):
        # canvas style
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetOptTitle(0)        

        self.c.SetLogz()
        self.c.SetTickx(1)
        self.c.SetTicky(1)

        self.c.SetRightMargin(0.19)
        self.c.SetTopMargin(0.08)
        self.c.SetLeftMargin(0.14)
        self.c.SetBottomMargin(0.14)

        # set x axis
        self.emptyHisto.GetXaxis().SetLabelFont(42)
        self.emptyHisto.GetXaxis().SetLabelSize(0.035)
        self.emptyHisto.GetXaxis().SetTitleFont(42)
        self.emptyHisto.GetXaxis().SetTitleSize(0.05)
        self.emptyHisto.GetXaxis().SetTitleOffset(1.2)
        self.emptyHisto.GetXaxis().SetTitle(self.model.sParticle)
        #self.emptyHisto.GetXaxis().CenterTitle(True)

        # set y axis
        self.emptyHisto.GetYaxis().SetLabelFont(42)
        self.emptyHisto.GetYaxis().SetLabelSize(0.035)
        self.emptyHisto.GetYaxis().SetTitleFont(42)
        self.emptyHisto.GetYaxis().SetTitleSize(0.05)
        self.emptyHisto.GetYaxis().SetTitleOffset(1.3)
        self.emptyHisto.GetYaxis().SetTitle(self.model.LSP)
        if hasattr(self.model, "Ndivisions"):
            self.emptyHisto.GetXaxis().SetNdivisions(self.model.Ndivisions)
        #self.emptyHisto.GetYaxis().CenterTitle(True)
                
    def DrawText(self):
        #redraw axes
        self.c.RedrawAxis()
        # white background
        graphWhite = rt.TGraph(5)
        graphWhite.SetName("white")
        graphWhite.SetTitle("white")
        graphWhite.SetFillColor(rt.kWhite)
        graphWhite.SetFillStyle(1001)
        graphWhite.SetLineColor(rt.kBlack)
        graphWhite.SetLineStyle(1)
        graphWhite.SetLineWidth(3)
        graphWhite.SetPoint(0,self.model.Xmin, self.model.Ymax)
        graphWhite.SetPoint(1,self.model.Xmax, self.model.Ymax)
        if(self.model.label2 == ""):
            graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.60)
            graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.60)
        else:
            graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.75)
            graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.75)
        graphWhite.SetPoint(4,self.model.Xmin, self.model.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
       	CMS_lumi.writeExtraText = 0
	CMS_lumi.extraText = self.preliminary
	CMS_lumi.lumi_13TeV = self.lumi+" fb^{-1}"

	CMS_lumi.lumi_sqrtS = self.energy+" TeV"  
	iPos=0
	CMS_lumi.CMS_lumi(self.c,4, iPos)
        # CMS LABEL
        textCMS = rt.TLatex(0.25,0.96,"  %s " %(self.preliminary))
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(52)
        textCMS.SetTextSize(0.033)
        textCMS.Draw()
        self.c.textCMS = textCMS
        # MODEL LABEL
        if(self.model.label2 == ""):
            textModelLabel= rt.TLatex(0.15,0.90,"%s   NLO+NLL exclusion" %self.model.label)
            textModelLabel.SetNDC()
            textModelLabel.SetTextAlign(13)
            textModelLabel.SetTextFont(42)
            textModelLabel.SetTextSize(0.02)
            textModelLabel.Draw()
            self.c.textModelLabel = textModelLabel
            #textModelLabel3= rt.TLatex(0.54,0.85,"m#kern[0.1]{_{#tilde{#chi_{1}}^{#pm}}} = 0.5m#kern[1.1]{_{#tilde{t}_{1}}} + 0.5m#kern[0.1]{_{#tilde{#chi_{1}}^{0}}}")
            #textModelLabel3.SetNDC()
            #textModelLabel3.SetTextAlign(13)
            #textModelLabel3.SetTextFont(42)
            #textModelLabel3.SetTextSize(0.03)
            #textModelLabel3.Draw()
            #self.c.textModelLabel3 = textModelLabel3
        else:
            textModelLabel= rt.TLatex(0.15,0.91,"%s   NLO+NLL exclusion" %self.model.label)
            textModelLabel.SetNDC()
            textModelLabel.SetTextAlign(13)
            textModelLabel.SetTextFont(42)
            textModelLabel.SetTextSize(0.035)
            textModelLabel.Draw()
            self.c.textModelLabel = textModelLabel
            textModelLabel2= rt.TLatex(0.15,0.86,"%s" %self.model.label2)
            textModelLabel2.SetNDC()
            textModelLabel2.SetTextAlign(13)
            textModelLabel2.SetTextFont(42)
            textModelLabel2.SetTextSize(0.035)
            textModelLabel2.Draw()
            self.c.textModelLabel2 = textModelLabel2

        # # NLO NLL XSEC
        # textNLONLL= rt.TLatex(0.16,0.32,"NLO-NLL exclusion")
        # textNLONLL.SetNDC()
        # textNLONLL.SetTextAlign(13)
        # textNLONLL.SetTextFont(42)
        # textNLONLL.SetTextSize(0.04)
        # textNLONLL.Draw()
        # #self.c.textNLONLL = textNLONLL

        if self.model.diagTopOn:
            # MTOP LABEL
            xT = getattr(self.model,"xTextTop",0.38)
            yT = getattr(self.model,"yTextTop",0.60)
            angleT = getattr(self.model,"angleTextTop",61)
            textMTop = rt.TLatex(xT,yT,"m_{#tilde{t}} = m_{t} + m_{#tilde{#chi}^{0}_{1}}")
            textMTop.SetNDC()
            textMTop.SetTextAlign(13)
            textMTop.SetTextFont(42)
            textMTop.SetTextSize(0.024)
            textMTop.SetTextAngle(angleT)
            textMTop.Draw()
            self.c.textMTop = textMTop

        if self.model.diagWOn:
            # LABEL MWtop
            xT = getattr(self.model,"xTextW",0.58)
            yT = getattr(self.model,"yTextW",0.70)
            angleT = getattr(self.model,"angleTextW",61)
            textMW = rt.TLatex(xT,yT,"m_{#tilde{t}} = m_{W} + m_{#tilde{#chi}^{0}_{1}}")
            textMW.SetNDC()
            textMW.SetTextAlign(13)
            textMW.SetTextFont(42)
            textMW.SetTextSize(0.024)
            textMW.SetTextAngle(angleT)
            textMW.Draw()
            self.c.textMW = textMW


        if getattr(self.model,"textT2qqOne",False):
            # LABEL T2qq single-squark degeneracy
            textOneSq = rt.TLatex(0.28,0.35,"one light #tilde{q}")
            textOneSq.SetNDC()
            textOneSq.SetTextAlign(13)
            textOneSq.SetTextFont(62)
            textOneSq.SetTextSize(0.034)
            textOneSq.Draw()
            self.c.textOneSq = textOneSq

        if getattr(self.model,"textT2qqEight",False):
            # LABEL T2qq single-squark degeneracy
            textEightSq = rt.TLatex(0.54,0.58,"#tilde{q}_{L} + #tilde{q}_{R} (#tilde{u},#tilde{d},#tilde{s},#tilde{c})")
            textEightSq.SetNDC()
            textEightSq.SetTextAlign(13)
            textEightSq.SetTextFont(62)
            textEightSq.SetTextSize(0.034)
            textEightSq.Draw()
            self.c.textEightSq = textEightSq


    def Save(self,label):
        # save the output
        self.c.SaveAs("%s.pdf" %label)
        
    def DrawLegend(self):
        if(self.model.label2 == ""):
            offset = 0
        else:
            offset = -50
        xRange = self.model.Xmax-self.model.Xmin
        yRange = self.model.Ymax-self.model.Ymin
        
        LObs = rt.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(color(self.OBS['colorLine']))
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10+offset)
        LObs.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10+offset)

        LObsP = rt.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        LObsP.SetLineColor(color(self.OBS['colorLine']))
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        LObsP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.20*yRange/100*10+offset)
        LObsP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.20*yRange/100*10+offset)

        LObsM = rt.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        LObsM.SetLineColor(color(self.OBS['colorLine']))
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        LObsM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.50*yRange/100*10+offset)
        LObsM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.50*yRange/100*10+offset)

        textObs = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10+offset, 
                            "Observed #pm 1 #sigma_{theory}")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
#        textObs.Draw()
        self.c.textObs = textObs

        LExpP = rt.TGraph(2)
        LExpP.SetName("LExpP")
        LExpP.SetTitle("LExpP")
        LExpP.SetLineColor(color(self.EXP['colorLine']))
        LExpP.SetLineStyle(7)
        LExpP.SetLineWidth(2)  
        LExpP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.85*yRange/100*10+offset)
        LExpP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.85*yRange/100*10+offset)

        LExp = rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(color(self.EXP['colorLine']))
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10+offset)
        LExp.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10+offset)
        
        LExpM = rt.TGraph(2)
        LExpM.SetName("LExpM")
        LExpM.SetTitle("LExpM")
        LExpM.SetLineColor(color(self.EXP['colorLine']))
        LExpM.SetLineStyle(7)
        LExpM.SetLineWidth(2)  
        LExpM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.15*yRange/100*10+offset)
        LExpM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.15*yRange/100*10+offset)

        if 'plus2' in self.EXP:
            LExpP2 = rt.TGraph(2)
            LExpP2.SetName("LExpP2")
            LExpP2.SetTitle("LExpP2")
            LExpP2.SetLineColor(color(self.EXP['colorLine']))
            LExpP2.SetLineStyle(3)
            LExpP2.SetLineWidth(2)  
            LExpP2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.70*yRange/100*10+offset)
            LExpP2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.70*yRange/100*10+offset)
        if 'minus2' in self.EXP:
            LExpM2 = rt.TGraph(2)
            LExpM2.SetName("LExpP2")
            LExpM2.SetTitle("LExpP2")
            LExpM2.SetLineColor(color(self.EXP['colorLine']))
            LExpM2.SetLineStyle(3)
            LExpM2.SetLineWidth(2)  
            LExpM2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.3*yRange/100*10+offset)
            LExpM2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.3*yRange/100*10+offset)


        if 'plus2' in self.EXP and len(self.EXP["plus2"])>0:
            textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10+offset,\
                                "Expected #pm 1 and 2 #sigma_{experiment}")
        else:
            textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10+offset,\
                    "Expected #pm 1 #sigma_{experiment}")

        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
        textExp.Draw()
        self.c.textExp = textExp

#        LObs.Draw("LSAME")
#        LObsM.Draw("LSAME")
#        LObsP.Draw("LSAME")
        LExp.Draw("LSAME")
        LExpM.Draw("LSAME")
        LExpP.Draw("LSAME")
        if 'plus2' in self.EXP and len(self.EXP['plus2'])>0:
            LExpP2.Draw("LSAME")
            self.c.LExpP2 = LExpP2
        if 'minus2' in self.EXP and len(self.EXP['minus2'])>0:
            LExpM2.Draw("LSAME")
            self.c.LExpM2 = LExpM2
        
        self.c.LObs = LObs
        self.c.LObsM = LObsM
        self.c.LObsP = LObsP
        self.c.LExp = LExp
        self.c.LExpM = LExpM
        self.c.LExpP = LExpP

    def DrawDiagonal(self):
        diagonal = rt.TGraph(3, self.model.diagX, self.model.diagY)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kGray)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.diagonal = diagonal


    def DrawDiagonalMTop(self):
        xs = array("d",[self.model.Xmin,(self.model.Xmax-self.model.Xmin)/2+self.model.Xmin,self.model.Xmax])
        ys = array("d",[x - 175. for x in xs])
        diagonal = rt.TGraph(3, xs, ys)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kGray)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.topDiagonal = diagonal

    def DrawDiagonalMW(self):
        xs = array("d",[self.model.Xmin,(self.model.Xmax-self.model.Xmin)/2+self.model.Xmin,self.model.Xmax])
        ys = array("d",[x - 80.4 for x in xs])
        diagonal = rt.TGraph(3, xs, ys)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kGray)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.wDiagonal = diagonal


    def DrawTopCorrPoly(self):
        xs = array("d",[150.+self.model.Ymin,200.+self.model.Ymin,287.5,262.5])
        ys = array("d",[self.model.Ymin,self.model.Ymin,87.5,112.5])
        trap = rt.TPolyLine(4,xs,ys)
        trap.SetFillColor(0)
        trap.SetLineColor(0)
        trap.Draw("FSAME")
        self.c.topCorr = trap

    def DrawLinesSimple(self):
        # observed
        for obj in self.OBS['nominal']:
            obj.SetLineColor(self.model.color)
            obj.SetLineStyle(1)
            obj.SetLineWidth(3)
        # expected
        for obj in self.EXP['nominal']:
            obj.SetLineColor(self.model.color)
            obj.SetLineStyle(7)
            obj.SetLineWidth(3)        
        # DRAW LINES
        for name,objs in self.EXP.iteritems():
            if name not in ['nominal']:
                continue
            for obj in objs:
                obj.Draw("LSAME")
        for name,objs in self.OBS.iteritems():
            if name not in ['nominal']:
                continue
            for obj in objs:
                obj.Draw("LSAME")

        
    def DrawLines(self):
        # observed
        for obj in self.OBS['nominal']:
            obj.SetLineColor(color(self.OBS['colorLine']))
            obj.SetLineStyle(1)
            obj.SetLineWidth(4)
        # observed + 1sigma
        for obj in self.OBS['plus']:
            obj.SetLineColor(color(self.OBS['colorLine']))
            obj.SetLineStyle(1)
            obj.SetLineWidth(2)        
        # observed - 1sigma
        for obj in self.OBS['minus']:
            obj.SetLineColor(color(self.OBS['colorLine']))
            obj.SetLineStyle(1)
            obj.SetLineWidth(2)        
        # expected + 1sigma
        for obj in self.EXP['plus']:
            obj.SetLineColor(color(self.EXP['colorLine']))
            obj.SetLineStyle(7)
            obj.SetLineWidth(2)                
        # expected + 2sigma
        for obj in self.EXP['plus2']:
            obj.SetLineColor(color(self.EXP['colorLine']))
            obj.SetLineStyle(3)
            obj.SetLineWidth(2)                
        # expected
        for obj in self.EXP['nominal']:
            obj.SetLineColor(color(self.EXP['colorLine']))
            obj.SetLineStyle(7)
            obj.SetLineWidth(4)        
        for obj in self.EXP['minus']:
            # expected - 1sigma
            obj.SetLineColor(color(self.EXP['colorLine']))
            obj.SetLineStyle(7)
            obj.SetLineWidth(2)                        
        # expected - 2sigma
        for obj in self.EXP['minus2']:
            obj.SetLineColor(color(self.EXP['colorLine']))
            obj.SetLineStyle(3)
            obj.SetLineWidth(2)                
        # DRAW LINES
        for name,objs in self.EXP.iteritems():
            if name not in ['nominal','plus','plus2','minus','minus2']:
                continue
            for obj in objs:
                obj.Draw("LSAME")
        for name,objs in self.OBS.iteritems():
            if name not in ['nominal','plus','plus2','minus','minus2']:
                continue
            for obj in objs:
                obj.Draw("LSAME")


        
