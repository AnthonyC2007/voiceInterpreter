{
    "patcher": {
        "fileversion": 1,
        "appversion": {
            "major": 9,
            "minor": 1,
            "revision": 2,
            "architecture": "x64",
            "modernui": 1
        },
        "classnamespace": "box",
        "rect": [ 686.0, 108.0, 784.0, 762.0 ],
        "boxes": [
            {
                "box": {
                    "id": "obj-2",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 124.5, 498.0, 41.0, 22.0 ],
                    "text": "set $1"
                }
            },
            {
                "box": {
                    "id": "obj-udp",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 30.0, 35.0, 140.0, 22.0 ],
                    "text": "udpreceive 7777"
                }
            },
            {
                "box": {
                    "id": "obj-route",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 30.0, 75.0, 120.0, 22.0 ],
                    "text": "route /emotion"
                }
            },
            {
                "box": {
                    "id": "obj-unpack",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 6,
                    "outlettype": [ "float", "float", "float", "float", "float", "float" ],
                    "patching_rect": [ 30.0, 120.0, 165.0, 22.0 ],
                    "text": "unpack f f f f f f"
                }
            },
            {
                "box": {
                    "id": "obj-m1",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 30.0, 160.0, 50.0, 22.0 ],
                    "text": "* 100."
                }
            },
            {
                "box": {
                    "id": "obj-m2",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 120.0, 160.0, 50.0, 22.0 ],
                    "text": "* 100."
                }
            },
            {
                "box": {
                    "id": "obj-m3",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 210.0, 160.0, 50.0, 22.0 ],
                    "text": "* 100."
                }
            },
            {
                "box": {
                    "id": "obj-m4",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 300.0, 160.0, 50.0, 22.0 ],
                    "text": "* 100."
                }
            },
            {
                "box": {
                    "id": "obj-m5",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 390.0, 160.0, 50.0, 22.0 ],
                    "text": "* 100."
                }
            },
            {
                "box": {
                    "id": "obj-m6",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 480.0, 160.0, 50.0, 22.0 ],
                    "text": "* 100."
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "format": 6,
                    "id": "obj-f1",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 30.0, 198.0, 60.0, 20.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "format": 6,
                    "id": "obj-f2",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 120.0, 198.0, 60.0, 20.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "format": 6,
                    "id": "obj-f3",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 210.0, 198.0, 60.0, 20.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "format": 6,
                    "id": "obj-f4",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 300.0, 198.0, 60.0, 20.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "format": 6,
                    "id": "obj-f5",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 390.0, 198.0, 60.0, 20.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "format": 6,
                    "id": "obj-f6",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 480.0, 198.0, 60.0, 20.0 ]
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.128, 0.128, 0.128, 1.0 ],
                    "id": "obj-s1",
                    "knobcolor": [ 0.502, 0.502, 0.502, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 30.0, 232.0, 55.0, 200.0 ],
                    "size": 100.0
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.128, 0.128, 0.128, 1.0 ],
                    "id": "obj-s2",
                    "knobcolor": [ 0.231, 0.545, 0.831, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 120.0, 232.0, 55.0, 200.0 ],
                    "size": 100.0
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.128, 0.128, 0.128, 1.0 ],
                    "id": "obj-s3",
                    "knobcolor": [ 0.545, 0.31, 0.831, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 210.0, 232.0, 55.0, 200.0 ],
                    "size": 100.0
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.128, 0.128, 0.128, 1.0 ],
                    "id": "obj-s4",
                    "knobcolor": [ 0.976, 0.796, 0.259, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 300.0, 232.0, 55.0, 200.0 ],
                    "size": 100.0
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.128, 0.128, 0.128, 1.0 ],
                    "id": "obj-s5",
                    "knobcolor": [ 0.239, 0.659, 0.329, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 390.0, 232.0, 55.0, 200.0 ],
                    "size": 100.0
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.128, 0.128, 0.128, 1.0 ],
                    "id": "obj-s6",
                    "knobcolor": [ 0.886, 0.294, 0.29, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 480.0, 232.0, 55.0, 200.0 ],
                    "size": 100.0
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "id": "obj-lbl1",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 30.0, 436.0, 60.0, 18.0 ],
                    "text": "neutral",
                    "textcolor": [ 0.502, 0.502, 0.502, 1.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "id": "obj-lbl2",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 120.0, 436.0, 60.0, 18.0 ],
                    "text": "sad",
                    "textcolor": [ 0.231, 0.545, 0.831, 1.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "id": "obj-lbl3",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 210.0, 436.0, 60.0, 18.0 ],
                    "text": "fear",
                    "textcolor": [ 0.545, 0.31, 0.831, 1.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "id": "obj-lbl4",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 300.0, 436.0, 60.0, 18.0 ],
                    "text": "happy",
                    "textcolor": [ 0.976, 0.796, 0.259, 1.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "id": "obj-lbl5",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 390.0, 436.0, 60.0, 18.0 ],
                    "text": "disgust",
                    "textcolor": [ 0.239, 0.659, 0.329, 1.0 ]
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "id": "obj-lbl6",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 480.0, 436.0, 60.0, 18.0 ],
                    "text": "angry",
                    "textcolor": [ 0.886, 0.294, 0.29, 1.0 ]
                }
            },
            {
                "box": {
                    "fontface": 1,
                    "fontsize": 13.0,
                    "id": "obj-dom-label",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 24.0, 543.5, 80.0, 21.0 ],
                    "text": "dominant:"
                }
            },
            {
                "box": {
                    "fontface": 1,
                    "fontsize": 14.0,
                    "id": "obj-dom-display",
                    "maxclass": "textedit",
                    "numinlets": 1,
                    "numoutlets": 4,
                    "outlettype": [ "", "int", "", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 115.0, 541.0, 240.0, 26.0 ],
                    "text": "\"sad  63%\""
                }
            },
            {
                "box": {
                    "id": "obj-js",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 620.0, 120.0, 150.0, 22.0 ],
                    "saved_object_attributes": {
                        "filename": "emotionlogic.js",
                        "parameter_enable": 0
                    },
                    "text": "js emotionlogic.js"
                }
            },
            {
                "box": {
                    "id": "obj-trig",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "bang", "" ],
                    "patching_rect": [ 620.0, 165.0, 40.0, 22.0 ],
                    "text": "t b l"
                }
            },
            {
                "box": {
                    "id": "obj-setall",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 700.0, 210.0, 130.0, 22.0 ],
                    "text": "setall $1 $2 $3"
                }
            },
            {
                "box": {
                    "id": "obj-jm",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "jit_matrix", "" ],
                    "patching_rect": [ 620.0, 260.0, 200.0, 22.0 ],
                    "text": "jit.matrix 3 char 300 300"
                }
            },
            {
                "box": {
                    "id": "obj-jpw",
                    "maxclass": "jit.pwindow",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "jit_matrix", "" ],
                    "patching_rect": [ 620.0, 310.0, 230.0, 230.0 ],
                    "sync": 1
                }
            },
            {
                "box": {
                    "fontsize": 10.0,
                    "id": "obj-col-label",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 620.0, 295.0, 100.0, 18.0 ],
                    "text": "colour blend"
                }
            },
            {
                "box": {
                    "fontface": 2,
                    "fontsize": 10.0,
                    "id": "obj-note",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 620.0, 100.0, 250.0, 18.0 ],
                    "text": "emotionlogic.js must be in the same folder"
                }
            },
            {
                "box": {
                    "fontface": 1,
                    "fontsize": 11.0,
                    "id": "obj-title",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 30.0, 8.0, 500.0, 19.0 ],
                    "text": "emotion visualiser v2  —  port 7777  —  bar chart + colour blend"
                }
            }
        ],
        "lines": [
            {
                "patchline": {
                    "destination": [ "obj-dom-display", 0 ],
                    "source": [ "obj-2", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-s1", 0 ],
                    "source": [ "obj-f1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-s2", 0 ],
                    "source": [ "obj-f2", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-s3", 0 ],
                    "source": [ "obj-f3", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-s4", 0 ],
                    "source": [ "obj-f4", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-s5", 0 ],
                    "source": [ "obj-f5", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-s6", 0 ],
                    "source": [ "obj-f6", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-jpw", 0 ],
                    "source": [ "obj-jm", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-2", 0 ],
                    "source": [ "obj-js", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-trig", 0 ],
                    "source": [ "obj-js", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-f1", 0 ],
                    "source": [ "obj-m1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-f2", 0 ],
                    "source": [ "obj-m2", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-f3", 0 ],
                    "source": [ "obj-m3", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-f4", 0 ],
                    "source": [ "obj-m4", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-f5", 0 ],
                    "source": [ "obj-m5", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-f6", 0 ],
                    "source": [ "obj-m6", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-js", 0 ],
                    "order": 0,
                    "source": [ "obj-route", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-unpack", 0 ],
                    "order": 1,
                    "source": [ "obj-route", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-jm", 0 ],
                    "source": [ "obj-setall", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-jm", 0 ],
                    "source": [ "obj-trig", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-setall", 0 ],
                    "source": [ "obj-trig", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-route", 0 ],
                    "source": [ "obj-udp", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-m1", 0 ],
                    "source": [ "obj-unpack", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-m2", 0 ],
                    "source": [ "obj-unpack", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-m3", 0 ],
                    "source": [ "obj-unpack", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-m4", 0 ],
                    "source": [ "obj-unpack", 3 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-m5", 0 ],
                    "source": [ "obj-unpack", 4 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-m6", 0 ],
                    "source": [ "obj-unpack", 5 ]
                }
            }
        ],
        "autosave": 0
    }
}