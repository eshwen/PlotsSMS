from array import *
import ROOT as rt

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname.find("T1qqqq") != -1: self.T1qqqq()
        if modelname.find("T1ttbb") != -1: self.T1ttbb()
        if modelname.find("T5ttttDM175") != -1: self.T5ttttDM175()
        if modelname.find("T5tttt-degen") != -1: self.T5tttt_degen()
        if modelname.find("T5ttcc") != -1: self.T5ttcc()
        if modelname.find("T2tt") != -1: self.T2tt()
        if modelname.find("T2cc") != -1: self.T2cc()
        if modelname.find("T2mixed") != -1: self.T2mixed()
        if modelname.find("T2-4bd") != -1: self.T24bd()
        if modelname.find("T2bb") != -1: self.T2bb()
        if modelname.find("T2qq") != -1: self.T2qq()
        if modelname.find("T2tb") != -1: self.T2tb()
        if modelname.find("T2bW-X05") != -1: self.T2bW_X05()



    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        self.color = rt.kRed
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} "+lsp_s;
        self.label2= "";
        # scan range to plot
        self.Xmin = 600.
        self.Xmax = 2000.
        self.Ymin = 0.
        self.Ymax = 1800.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False
                
    def T1qqqq(self):
        # model name
        self.modelname = "T1qqqq"
        # decay chain
        self.color = rt.kBlue
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow q #bar{q} "+lsp_s;
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 2000
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False

    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        self.color = rt.kBlue
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow b #bar{b} "+lsp_s;
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600.
        self.Xmax = 2100.
        self.Ymin = 0.
        self.Ymax = 1800.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False


    def T1ttbb(self):
        # model name
        self.modelname = "T1ttbb"
        self.color = rt.kGreen+3
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}";
        #self.label2= "(m_{#tilde{#chi}_{1}^{0}} - m_{#tilde{#chi}^{0}_{1}} - m_{#tilde{#chi}^{0}_{1}} = 5 GeV)";
        self.label2= "#tilde{g} #rightarrow t b #tilde{#chi}^{#pm}_{1}, #tilde{#chi}^{#pm}_{1} #rightarrow W#kern[0.1]{*}#tilde{#chi}^{0}_{1} (m_{#tilde{#chi}^{#pm}_{1}} - m_{#tilde{#chi}^{0}_{1}} = 5 GeV)";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600.
        self.Xmax = 1950.
        self.Ymin = 0.
        self.Ymax = 1600.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False

    def T5ttttDM175(self):
        # model name
        self.modelname = "T5ttttDM175"
        # decay chain
        self.color = rt.kRed
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}"
        self.label2 = "#tilde{g} #rightarrow #tilde{t}_{1} t,  #tilde{t}_{1} #rightarrow #bar{t} "+lsp_s+" (m#kern[0.1]{_{#tilde{t}_{1}}} - m_{#tilde{#chi}^{0}_{1}} = 175 GeV)";
        # scan range to plot
        self.Xmin = 600.
        self.Xmax = 1700.
        self.Ymin = 50.
        self.Ymax = 1600.
        self.Zmin = 0.1
        self.Zmax = 100.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False


    def T5tttt_degen(self):
        # model name
        self.modelname = "T5tttt_degen"
        self.color = rt.kGreen+3
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}"
        self.label2= "#tilde{g} #rightarrow #tilde{t}_{1} t,  #tilde{t}_{1} #rightarrow b f f "+lsp_s+" (m#kern[0.1]{_{#tilde{t}_{1}}} - m_{#tilde{#chi}^{0}_{1}} = 20 GeV)";
        # scan range to plot
        self.Xmin = 600.
        self.Xmax = 1700.
        self.Ymin = 0.
        self.Ymax = 1600.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False

    def T5ttcc(self):
        # model name
        self.modelname = "T5ttcc"
        self.color = rt.kBlue
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #tilde{t}_{1},"
        self.label2= "#tilde{t}_{1} #rightarrow c "+lsp_s+" (m#kern[0.1]{_{#tilde{t}_{1}}} - m_{#tilde{#chi}^{0}_{1}} = 20 GeV)"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600.
        self.Xmax = 1700.
        self.Ymin = 0.
        self.Ymax = 1600.
        self.Zmin = 0.01
        self.Zmax = 300.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False

    def T2tt(self):
        # model name
        self.modelname = "T2tt"
        self.color = rt.kRed
        #self.color = rt.kCyan+2
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{t}_{1} #tilde{t}_{1}, #tilde{t}_{1} #rightarrow t #tilde{#chi}^{0}_{1}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 150.
        self.Xmax = 1200.
        self.Ymin = 0.
        self.Ymax = 700.
        self.Zmin = 0.001
        self.Zmax = 100.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{t}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = True
        self.blankTopCorr = True
        self.diagWOn = False
        # more specs on the text
        self.xTextTop = 0.38
        self.yTextTop = 0.50
        self.angleTextTop = 61


    def T2cc(self):
        # model name
        self.modelname = "T2cc"
        self.color = rt.kCyan-3
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{t}_{1} #tilde{t}_{1}, #tilde{t}_{1} #rightarrow c #tilde{#chi}^{0}_{1}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 250.
        self.Xmax = 600.
        self.Ymin = 175.
        self.Ymax = 800.
        self.Zmin = 0.5
        self.Zmax = 20.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{t}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = True
        # more specs on the text
        self.xTextW = 0.50
        self.yTextW = 0.38
        self.angleTextW = 33



    def T24bd(self):
        # model name
        self.modelname = "T2-4bd"
        #self.color = rt.kRed-3
        self.color = rt.kViolet-1
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{t}_{1} #tilde{t}_{1}, #tilde{t}_{1} #rightarrow b f f' #tilde{#chi}^{0}_{1}";
        self.label2= "4-body phase space";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 100.
        self.Xmax = 600.
        self.Ymin = 0.
        self.Ymax = 750.
        self.Zmin = 0.5
        self.Zmax = 100.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{t}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = True
        # more specs on the text
        self.xTextW = 0.53
        self.yTextW = 0.48
        self.angleTextW = 38


    def T2mixed(self):
        # model name
        self.modelname = "T2mixed"
        self.color = rt.kOrange-1
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "#scale[0.85]{pp #rightarrow #tilde{t}_{1} #tilde{t}_{1}, #tilde{t}_{1} #rightarrow c #tilde{#chi}^{0}_{1}/b f f' #tilde{#chi}^{0}_{1}}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 100.
        self.Xmax = 550.
        self.Ymin = 0.
        self.Ymax = 750.
        self.Zmin = 0.5
        self.Zmax = 100.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{t}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = True
        # more specs on the text
        self.xTextW = 0.65
        self.yTextW = 0.53
        self.angleTextW = 35


    def T2bb(self):
        # model name
        self.modelname = "T2bb"
        self.color = rt.kBlue
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{b}_{1} #tilde{b}_{1}, #tilde{b}_{1} #rightarrow b #tilde{#chi}^{0}_{1}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 300.
        self.Xmax = 1200.
        self.Ymin = 0.
        self.Ymax = 800.
        self.Zmin = 0.001
        self.Zmax = 20.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{b}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False

    def T2qq(self):
        # model name
        self.modelname = "T2qq"
        self.color = rt.kRed
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{q}_{1} #tilde{q}_{1}, #tilde{q}_{1} #rightarrow q #tilde{#chi}^{0}_{1}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 300.
        self.Xmax = 1600.
        self.Ymin = 0.
        self.Ymax = 1200.
        self.Zmin = 0.001
        self.Zmax = 5.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{q}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False
        self.textT2qqOne = True
        self.textT2qqEight = True


    def T2tb(self):
        # model name
        self.modelname = "T2tb"
        #self.color = rt.kYellow+1
        self.color = rt.kGreen + 3
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{t}_{1} #tilde{t}_{1}, #tilde{t}_{1} #rightarrow t #tilde{#chi}^{0}_{1}/b #tilde{#chi}^{#pm}_{1}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 200.
        self.Xmax = 900.
        self.Ymin = 0.
        self.Ymax = 600.
        self.Zmin = 0.01
        self.Zmax = 100.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{t}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = True
        self.blankTopCorr = False
        self.diagWOn = False
        # more specs on the text
        self.xTextTop = 0.38
        self.yTextTop = 0.52
        self.angleTextTop = 53


    def T2bW_X05(self):
        # model name
        self.modelname = "T2bW_X05"
        self.color = rt.kGreen+3
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{t}_{1} #tilde{t}_{1}, #tilde{t}_{1} #rightarrow b #tilde{#chi}_{1}^{#pm}#rightarrow b #tilde{#chi}_{1}^{0} W#kern[0.1]{^{(*)}}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 200.
        self.Xmax = 900.
        self.Ymin = 0.
        self.Ymax = 450.
        self.Zmin = 0.01
        self.Zmax = 100.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{t}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagTopOn = False
        self.blankTopCorr = False
        self.diagWOn = False
        # more specs on the text
        self.xTextTop = 0.38
        self.yTextTop = 0.52
        self.angleTextTop = 53
