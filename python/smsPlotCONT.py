import ROOT as rt
from array import *
from sms import *
from color import *
from smsPlotABS import *

# class producing the 2D plot with contours
class smsPlotCONT(smsPlotABS):

    def __init__(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary, label,makeHisto=True):
        self.LABEL = label
        self.standardDef(modelname, histo, obsLimits, expLimits, energy, lumi, preliminary,makeHisto)
        # canvas for the plot
        if makeHisto:
            self.c = rt.TCanvas("cCONT_%s" %label,"cCONT_%s" %label,600,600)
            self.histo = self.emptyHistogram(histo)
            # canvas style

    # empty copy of the existing histogram
    def emptyHistogram(self, h):
        return rt.TH2D("%sEMPTY" %h['histogram'].GetName(), "%sEMPTY" %h['histogram'].GetTitle(),
                       h['histogram'].GetXaxis().GetNbins(), h['histogram'].GetXaxis().GetXmin(), h['histogram'].GetXaxis().GetXmax(),
                       h['histogram'].GetYaxis().GetNbins(), h['histogram'].GetYaxis().GetXmin(), h['histogram'].GetYaxis().GetXmax())
                                       
    def Draw(self,simple=False):
        self.setStyle()
        self.emptyHisto.Draw()
        self.histo.Draw("SAME")
        if self.model.diagOn:
            self.DrawDiagonal()
        # self.DrawObsArea()
        if simple:
            self.DrawLinesSimple()
        else:
            self.DrawLines()
        if not simple:
            if self.model.blankTopCorr:    
                self.DrawTopCorrPoly()
            if self.model.diagTopOn:
                self.DrawDiagonalMTop()
            if self.model.diagWOn:
                self.DrawDiagonalMW()

        #self.DrawText()
        #self.DrawLegend()

