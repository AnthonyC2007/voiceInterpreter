{
	"patcher" : {
		"fileversion" : 1,
		"appversion" : {
			"major" : 9,
			"minor" : 0,
			"bugfix" : 0,
			"type" : "Release",
			"track" : 0,
			"label" : ""
		},
		"rect" : [ 100.0, 100.0, 780.0, 560.0 ],
		"bglocked" : 0,
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"boxes" : [
			{
				"box" : {
					"id" : "obj-title",
					"maxclass" : "comment",
					"text" : "emotion visualiser v2  —  port 7777  —  bar chart + colour blend",
					"patching_rect" : [ 30.0, 8.0, 500.0, 20.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontface" : 1,
					"fontsize" : 11.0
				}
			},
			{
				"box" : {
					"id" : "obj-udp",
					"maxclass" : "newobj",
					"text" : "udpreceive 7777",
					"patching_rect" : [ 30.0, 35.0, 140.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ]
				}
			},
			{
				"box" : {
					"id" : "obj-route",
					"maxclass" : "newobj",
					"text" : "route /emotion",
					"patching_rect" : [ 30.0, 80.0, 120.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ]
				}
			},
			{
				"box" : {
					"id" : "obj-unpack",
					"maxclass" : "newobj",
					"text" : "unpack f f f f f f",
					"patching_rect" : [ 30.0, 130.0, 165.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 6,
					"outlettype" : [ "float", "float", "float", "float", "float", "float" ]
				}
			},
			{
				"box" : {
					"id" : "obj-m1",
					"maxclass" : "newobj",
					"text" : "* 100.",
					"patching_rect" : [ 30.0, 175.0, 50.0, 22.0 ],
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ]
				}
			},
			{
				"box" : {
					"id" : "obj-m2",
					"maxclass" : "newobj",
					"text" : "* 100.",
					"patching_rect" : [ 112.0, 175.0, 50.0, 22.0 ],
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ]
				}
			},
			{
				"box" : {
					"id" : "obj-m3",
					"maxclass" : "newobj",
					"text" : "* 100.",
					"patching_rect" : [ 194.0, 175.0, 50.0, 22.0 ],
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ]
				}
			},
			{
				"box" : {
					"id" : "obj-m4",
					"maxclass" : "newobj",
					"text" : "* 100.",
					"patching_rect" : [ 276.0, 175.0, 50.0, 22.0 ],
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ]
				}
			},
			{
				"box" : {
					"id" : "obj-m5",
					"maxclass" : "newobj",
					"text" : "* 100.",
					"patching_rect" : [ 358.0, 175.0, 50.0, 22.0 ],
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ]
				}
			},
			{
				"box" : {
					"id" : "obj-m6",
					"maxclass" : "newobj",
					"text" : "* 100.",
					"patching_rect" : [ 440.0, 175.0, 50.0, 22.0 ],
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ]
				}
			},
			{
				"box" : {
					"id" : "obj-f1",
					"maxclass" : "flonum",
					"patching_rect" : [ 30.0, 218.0, 65.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "float", "bang" ]
				}
			},
			{
				"box" : {
					"id" : "obj-f2",
					"maxclass" : "flonum",
					"patching_rect" : [ 112.0, 218.0, 65.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "float", "bang" ]
				}
			},
			{
				"box" : {
					"id" : "obj-f3",
					"maxclass" : "flonum",
					"patching_rect" : [ 194.0, 218.0, 65.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "float", "bang" ]
				}
			},
			{
				"box" : {
					"id" : "obj-f4",
					"maxclass" : "flonum",
					"patching_rect" : [ 276.0, 218.0, 65.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "float", "bang" ]
				}
			},
			{
				"box" : {
					"id" : "obj-f5",
					"maxclass" : "flonum",
					"patching_rect" : [ 358.0, 218.0, 65.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "float", "bang" ]
				}
			},
			{
				"box" : {
					"id" : "obj-f6",
					"maxclass" : "flonum",
					"patching_rect" : [ 440.0, 218.0, 65.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "float", "bang" ]
				}
			},
			{
				"box" : {
					"id" : "obj-c1",
					"maxclass" : "comment",
					"text" : "neutral",
					"patching_rect" : [ 30.0, 243.0, 65.0, 18.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontsize" : 10.0
				}
			},
			{
				"box" : {
					"id" : "obj-c2",
					"maxclass" : "comment",
					"text" : "sad",
					"patching_rect" : [ 112.0, 243.0, 65.0, 18.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontsize" : 10.0
				}
			},
			{
				"box" : {
					"id" : "obj-c3",
					"maxclass" : "comment",
					"text" : "fear",
					"patching_rect" : [ 194.0, 243.0, 65.0, 18.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontsize" : 10.0
				}
			},
			{
				"box" : {
					"id" : "obj-c4",
					"maxclass" : "comment",
					"text" : "happy",
					"patching_rect" : [ 276.0, 243.0, 65.0, 18.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontsize" : 10.0
				}
			},
			{
				"box" : {
					"id" : "obj-c5",
					"maxclass" : "comment",
					"text" : "disgust",
					"patching_rect" : [ 358.0, 243.0, 65.0, 18.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontsize" : 10.0
				}
			},
			{
				"box" : {
					"id" : "obj-c6",
					"maxclass" : "comment",
					"text" : "angry",
					"patching_rect" : [ 440.0, 243.0, 65.0, 18.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontsize" : 10.0
				}
			},
			{
				"box" : {
					"id" : "obj-ms",
					"maxclass" : "multislider",
					"patching_rect" : [ 30.0, 268.0, 460.0, 150.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"size" : 6,
					"style" : 1,
					"setminmax" : [ 0.0, 1.0 ],
					"contdata" : 0,
					"candicane" : 0
				}
			},
			{
				"box" : {
					"id" : "obj-jsnote",
					"maxclass" : "comment",
					"text" : "colorblend.js must be in the same folder as this patch",
					"patching_rect" : [ 530.0, 108.0, 240.0, 18.0 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"fontsize" : 10.0,
					"fontface" : 2
				}
			},
			{
				"box" : {
					"id" : "obj-js",
					"maxclass" : "newobj",
					"text" : "js colorblend.js",
					"patching_rect" : [ 530.0, 130.0, 130.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ]
				}
			},
			{
				"box" : {
					"id" : "obj-trig",
					"maxclass" : "newobj",
					"text" : "t b l",
					"patching_rect" : [ 530.0, 180.0, 40.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "" ]
				}
			},
			{
				"box" : {
					"id" : "obj-setall",
					"maxclass" : "message",
					"text" : "setall $1 $2 $3",
					"patching_rect" : [ 620.0, 225.0, 120.0, 22.0 ],
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ]
				}
			},
			{
				"box" : {
					"id" : "obj-jm",
					"maxclass" : "newobj",
					"text" : "jit.matrix 3 char 300 300",
					"patching_rect" : [ 530.0, 270.0, 200.0, 22.0 ],
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "jit_matrix" ]
				}
			},
			{
				"box" : {
					"id" : "obj-jpw",
					"maxclass" : "jit.pwindow",
					"patching_rect" : [ 530.0, 320.0, 210.0, 210.0 ],
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "jit_matrix", "", "" ]
				}
			}
		],
		"lines" : [
			{
				"patchline" : {
					"source" : [ "obj-udp", 0 ],
					"destination" : [ "obj-route", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-route", 0 ],
					"destination" : [ "obj-unpack", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-route", 0 ],
					"destination" : [ "obj-ms", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-route", 0 ],
					"destination" : [ "obj-js", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-unpack", 0 ],
					"destination" : [ "obj-m1", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-unpack", 1 ],
					"destination" : [ "obj-m2", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-unpack", 2 ],
					"destination" : [ "obj-m3", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-unpack", 3 ],
					"destination" : [ "obj-m4", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-unpack", 4 ],
					"destination" : [ "obj-m5", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-unpack", 5 ],
					"destination" : [ "obj-m6", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-m1", 0 ],
					"destination" : [ "obj-f1", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-m2", 0 ],
					"destination" : [ "obj-f2", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-m3", 0 ],
					"destination" : [ "obj-f3", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-m4", 0 ],
					"destination" : [ "obj-f4", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-m5", 0 ],
					"destination" : [ "obj-f5", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-m6", 0 ],
					"destination" : [ "obj-f6", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-js", 0 ],
					"destination" : [ "obj-trig", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-trig", 1 ],
					"destination" : [ "obj-setall", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-trig", 0 ],
					"destination" : [ "obj-jm", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-setall", 0 ],
					"destination" : [ "obj-jm", 0 ]
				}
			},
			{
				"patchline" : {
					"source" : [ "obj-jm", 0 ],
					"destination" : [ "obj-jpw", 0 ]
				}
			}
		]
	}
}
