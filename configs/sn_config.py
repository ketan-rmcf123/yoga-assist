import os

stages ={
0: [42, "Intro-Pranamasana"],
1: [147, "Hasta Uttanasana"],
2: [185, "Hasta Padasana"],
3: [220, "Ashwa Sanchalanasana"],
4: [250, "Dandasana"],
5: [287, "Ashtanga Namaskara"],
6: [313, "Bhujangasana"],
7: [345, "Parvatasana"],
8: [390, "Ashwa Sanchalanasana"],
9: [410, "Hasta Padasana"],
10: [417, "Hasta Uttanasana"],
11: [430, "Pranamasana"],

}
EXPECTED_ANGLES = {
   "Intro-Pranamasana" : {
     "ID": 1,
    "Angles" : {'left_elbow': 150.104337566288, 'right_elbow': 150.54342950085257, 'left_shoulder': 30.454155973970376, 'right_shoulder': 30.20323775494265, 'left_hip': 180.4113514554364, 'right_hip': 180.43829466743296, 'left_knee': 180.31233834231756, 'right_knee': 180.54702507121294, 'left_ankle': 105.96790903265024, 'right_ankle': 105.66477562336291}

#     "Angles" : {'left_elbow': 43.104337566288, 'right_elbow': 36.54342950085257, 'left_shoulder': -20.454155973970376, 'right_shoulder': -30.20323775494265, 'left_hip': -176.4113514554364, 'right_hip': 179.43829466743296, 'left_knee': -177.31233834231756, 'right_knee': -176.54702507121294, 'left_ankle': 104.96790903265024, 'right_ankle': 107.66477562336291}
    },
    "Hasta Uttanasana": {
     "ID": 2,
     "Angles" : {'left_elbow': -150.6059890473906, 'right_elbow': 174.4540676523918, 'left_shoulder': 179.9438827020537, 'right_shoulder': 174.98587251323355, 'left_hip': -176.21270640126187, 'right_hip': -174.2570887638874, 'left_knee': -150.33870110841164, 'right_knee': -155.18559596368192, 'left_ankle': 86.13311152045152, 'right_ankle': 91.95203745202765}
    },
    "Hasta Padasana": {
     "ID": 3,
     "Angles" : {'left_elbow': 177.04663423247698, 'right_elbow': 166.780695028459, 'left_shoulder': -118.5961280437309, 'right_shoulder': -119.97483791922944, 'left_hip': 36.62764028865011, 'right_hip': 37.43741102612372, 'left_knee': -174.21895137869222, 'right_knee': -176.63353933657018, 'left_ankle': 119.19552547326504, 'right_ankle': 118.21335577704295}
    },
    "Ashwa Sanchalanasana": {
     "ID": 4,
     "Angles" : {'left_elbow': 162.32222004213656, 'right_elbow': 168.91568470798595, 'left_shoulder': -27.690676567474224, 'right_shoulder': -40.95948809991859, 'left_hip': 37.26330817638441, 'right_hip': -155.93101341663095, 'left_knee': -64.30835846244041, 'right_knee': -128.73072947533072, 'left_ankle': 119.31913905478304, 'right_ankle': 85.29662622762912}
   },
    "Dandasana": {
     "ID": 5,
     "Angles" : {'left_elbow': 88.32760563891074, 'right_elbow': 88.52086019769396, 'left_shoulder': -3.6285321554364476, 'right_shoulder': -1.448645194846549, 'left_hip': 175.5175289451629, 'right_hip': -179.4678130022972, 'left_knee': -178.4391130880871, 'right_knee': 174.9236448329197, 'left_ankle': 133.7550792573758, 'right_ankle': 134.03551569777346}
    },
    "Ashtanga Namaskara": {
     "ID": 6,
     "Angles" : {'left_elbow': -52.346928070292414, 'right_elbow': -39.51007841974187, 'left_shoulder': 8.089380413952982, 'right_shoulder': -1.3446155881607258, 'left_hip': -114.85700294410474, 'right_hip': -117.2485909536535, 'left_knee': 126.35073577178875, 'right_knee': 132.1005711301755, 'left_ankle': -100.43932832416218, 'right_ankle': -104.19289592655976}
   },
    "Bhujangasana": {
     "ID": 7,
     "Angles" : {'left_elbow': 83.94991098771825, 'right_elbow': 78.24245335511924, 'left_shoulder': 12.283801998491686, 'right_shoulder': 20.93808860250694, 'left_hip': -162.36247841485005, 'right_hip': -159.36995025489293, 'left_knee': -173.79255532251233, 'right_knee': -174.58979589024202, 'left_ankle': 155.4768483243407, 'right_ankle': 158.1927695465329}
    },
    "Parvatasana": {
     "ID": 8,
     "Angles" : {'left_elbow': 160.0420821251495, 'right_elbow': 156.76710064044462, 'left_shoulder': -171.0812830127923, 'right_shoulder': -166.4942578487473, 'left_hip': 51.92838803361884, 'right_hip': 50.68513458302884, 'left_knee': -148.14790312107363, 'right_knee': -144.05777378335833, 'left_ankle': 96.43674922951587, 'right_ankle': 92.84213788365567}
    },
    "Ashwa Sanchalanasana": {
     "ID": 9,
     "Angles" : {'left_elbow': 162.32222004213656, 'right_elbow': 168.91568470798595, 'left_shoulder': -27.690676567474224, 'right_shoulder': -40.95948809991859, 'left_hip': 37.26330817638441, 'right_hip': -155.93101341663095, 'left_knee': -64.30835846244041, 'right_knee': -128.73072947533072, 'left_ankle': 119.31913905478304, 'right_ankle': 85.29662622762912}
   },
    "Hasta Padasana": {
     "ID": 10,
     "Angles" : {'left_elbow': 177.04663423247698, 'right_elbow': 166.780695028459, 'left_shoulder': -118.5961280437309, 'right_shoulder': -119.97483791922944, 'left_hip': 36.62764028865011, 'right_hip': 37.43741102612372, 'left_knee': -174.21895137869222, 'right_knee': -176.63353933657018, 'left_ankle': 119.19552547326504, 'right_ankle': 118.21335577704295}
    },
    "Hasta Uttanasana": {
     "ID": 11,
     "Angles" : {'left_elbow': -150.6059890473906, 'right_elbow': 174.4540676523918, 'left_shoulder': 179.9438827020537, 'right_shoulder': 174.98587251323355, 'left_hip': -176.21270640126187, 'right_hip': -174.2570887638874, 'left_knee': -150.33870110841164, 'right_knee': -155.18559596368192, 'left_ankle': 86.13311152045152, 'right_ankle': 91.95203745202765}
    },
    "Pranamasana": {
     "ID": 12,
     "Angles" : {'left_elbow': 42.104337566288, 'right_elbow': 36.54342950085257, 'left_shoulder': -20.454155973970376, 'right_shoulder': -30.20323775494265, 'left_hip': -176.4113514554364, 'right_hip': 179.43829466743296, 'left_knee': -177.31233834231756, 'right_knee': -176.54702507121294, 'left_ankle': 104.96790903265024, 'right_ankle': 107.66477562336291}
    },

}
yoga_sessions = [
    {
        "title": "Suryanamaskar",
        "summary": "Welcome to your personalized guide for Suryanamaskar.Let's flow through 10 energizing steps to kickstart your day!",
        "image": os.getcwd() + "\\bin\suryanamaskar.jpg",
        "streak": "8 Days",
        "level": "Easy",
    },
    {
        "title": "Restorative Flow",
        "summary": "Welcome to your personalized guide for Restorative asanas.Unwind and recharge with this super relaxing sequence.",
        "image": os.getcwd() +"\\bin\\restorative_flow.jpg",
        "streak": "8 Days",
        "level": "Easy",
    },
    {
        "title": "Ashtanga Yoga",
        "summary": "Welcome to your personalized guide for Ashtanga asanas.Dive into a powerful practice to build strength and feel amazing.",
        "image": os.getcwd() + "\\bin\\ashtanga.jpeg",
        "streak": "8 Days",
        "level": "Advanced",
    },
]