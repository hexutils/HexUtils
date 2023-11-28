# MELAcalc_v2.py

`MELAcalc_v2.py` is currently fully tested in JSON format. Within this format, `MELAcalc_v2` has the following options:


A sample input is provided for you here. Explanations for each field are provided further down.
```json
{
    "ghz1":{
        "Process":"SelfDefine_spin0",
        "Production":"ZZGG",
        "MatrixElement":"JHUGen",
        "Couplings":{
            "ghg2":[1,0],
            "ghz1":[1,0],
            "ghz4":[0,0],
            "reZ":[1,0],
            "leZ":[1,0]
        },
        "Prod":false,
        "Dec":true,
        "Particles":[
            [23, 3.09689, 0.0009],
            [25, 6.78, 0.161]
        ],
        "Options":{
            "DivideP":"ghz1",
            "MatchmH":"M4L"
        }
    },

    "ghz4":{
        "Process":"SelfDefine_spin0",
        "Production":"ZZGG",
        "MatrixElement":"JHUGen",
        "Couplings":{
            "ghg2":[1,0],
            "ghz1":[0,0],
            "ghz4":[1,0],
            "reZ":[1,0],
            "leZ":[1,0]
        },
        "Prod":false,
        "Dec":true,
        "Particles":[
            [23, 3.09689, 0.0009],
            [25, 6.78, 0.161]
        ],
        "Options":{
            "DivideP":"ghz1",
            "MatchmH":"M4L"
        }
    }
}
```


## Required Logistic Inputs

### Process

The Process is the physical process you are running. The possible processes can be seen below:
```python
VALID_PROCESS = {
    "HSMHiggs", #// Call this for any MCFM |H|**2-only ME.
    "H0_g1prime2",
    "H0hplus",
    "H0minus",
    "H0_Zgsg1prime2",
    "H0_Zgs",
    "H0_Zgs_PS",
    "H0_gsgs",
    "H0_gsgs_PS",

    "D_g1g1prime2",
    "D_g1g2",
    "D_g1g2_pi_2",
    "D_g1g4",
    "D_g1g4_pi_2",
    "D_zzzg",
    "D_zzgg",
    "D_zzzg_PS",
    "D_zzgg_PS",
    "D_zzzg_g1prime2",
    "D_zzzg_g1prime2_pi_2",

    "H1minus", #// 1-
    "H1plus", #// 1+

    "H2_g1", #// 2m+, Zg, gg
    "H2_g2", #// 2h2+
    "H2_g3", #// 2h3+
    "H2_g4", #// 2h+
    "H2_g5", #// 2b+
    "H2_g1g5", #// 2m+
    "H2_g6", #// 2h6+
    "H2_g7", #// 2h7+
    "H2_g8", #// 2h-
    "H2_g9", #// 2h9-
    "H2_g10", #// 2h10-

    "bkgGammaGamma", #// gamma+gamma cont.
    "bkgZGamma", #// Z+gamma cont.
    "bkgZJets", #// Z + 0/1/2 jets (ZZGG, JQCD, JJQCD)
    "bkgZZ", #// qq/gg->ZZ cont.
    "bkgWW", #// qq/gg->WW cont.
    "bkgWWZZ", #// gg->ZZ+WW cont.

    "bkgZZ_SMHiggs", #// ggZZ cont. + SMHigg
    "bkgWW_SMHiggs", #// ggWW cont. + SMHiggs
    "bkgWWZZ_SMHiggs", #// ggZZ+WW cont. + SMHiggs

    "HSMHiggs_WWZZ", #// MCFM |H|**2 ZZ+WW with ZZ-WW interference

    # /**** For width ***/
    "D_gg10",

    # /***** Self Defined******/
    "SelfDefine_spin0",
    "SelfDefine_spin1",
    "SelfDefine_spin2",
}
```

### Production

The production is how the particle is being produced. The possible production modes are below:
```python
VALID_PRODUCTION = {
    "ZZGG",
    "ZZQQB",
    "ZZQQB_STU", #// Should be the same as ZZQQB, just for crosscheck
    "ZZINDEPENDENT",

    "ttH", #// ttH
    "bbH", #// bbH

    "JQCD", #// ? + 1 jet

    "JJQCD",# // SBF
    "JJVBF",# // VBF
    "JJEW",# // VBF+VH (had.)
    "JJEWQCD",# // VBF+VH+QCD, all hadronic
    "Had_ZH",# // ZH, Z->uu/dd
    "Had_WH",# // W(+/-)H, W->ud
    "Lep_ZH",# // ZH, Z->ll/nunu
    "Lep_WH",# // W(+/-)H, W->lnu

    # // s-channel contributions
    "ZZQQB_S",
    "JJQCD_S",
    "JJVBF_S",
    "JJEW_S",
    "JJEWQCD_S",
    "Had_ZH_S",
    "Had_WH_S",
    "Lep_ZH_S",
    "Lep_WH_S",

    # // t+u-channel contributions
    "ZZQQB_TU",
    "JJQCD_TU",
    "JJVBF_TU",
    "JJEW_TU",
    "JJEWQCD_TU",
    "Had_ZH_TU",
    "Had_WH_TU",
    "Lep_ZH_TU",
    "Lep_WH_TU",

    "GammaH", #// gammaH, stable A (could implement S and TU in the future
}
```

### MatrixElement

The matrix element determines what is being used to evaluate probabilities. The possibilities are listed below:
```python
VALID_MATRIXELEMENT = {
    "MCFM",
    "JHUGen",
    "ANALYTICAL"
}
```

### Prod

Prod should be set to ```true``` if you are calculating production probabilities. Otherwise set it to ```false```.

### Dec

Dec should be set to ```true``` if you are calculating decay probabilities. Otherwise set it to ```false```.

## Couplings

Each coupling has an input as `<coupling name>:[<real>, <imaginary>]` for its value
Couplings are formatted as such. ___NOTE: COUPLING NAMES ARE CASE SENSITIVE___:
```json
"Couplings":{
    "ghg2":[1,0],
    "ghz1":[1,0],
    "reZ":[1,0]
}
```

## Particles

Particles is a list of particles whose mass you want to change. This is done by detailing a list of 3 items - one list for each particle you are changing. The list is formatted as such:
```json
"Particles":[
    [id, mass, width],
    [id, mass, width]
]
```

## Options Tag

### DivideP

The DivideP option divides the probabilities calculated for that branch by the probability name you choose. For instance, if DivideP is set to ```p_Gen_JJEW_SIG_ghv1_1_MCFM```, then the probability for that setup will be divided at the end by the probabilities from ```p_Gen_JJEW_SIG_ghv1_1_MCFM```.

### MatchmH

The matchmH option forces the mass and width for MELA to be set to a mass indicated by the branch. For instance, if matchmH is set to "M4L" then the mass of the Higgs will always be set to the M4L value corresponding to the same event.

### JetpT

Set this option if you want to change where the Jetpt branch is pulling from. Utilize this for systematics on your jets (jetpT JES_UP, JES_DOWN, etc.)

