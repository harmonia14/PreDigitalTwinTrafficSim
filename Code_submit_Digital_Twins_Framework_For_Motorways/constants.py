import json
import math

sumoBinary = "sumo-gui"
SUMO_CMD =[sumoBinary, "-c", "../ITSC2020_CAV_impact/Motorway/Simulations/Base/M50_simulation.sumo.cfg",
            "--statistic-output", "statistic.xml", "--tripinfo-output", "tripinfo.xml", "--tripinfo-output.write-unfinished", "--delay", "1000", "--full-output", "fulloutput.xml"]
DECODING = (lambda v: json.loads(v))
BROKER1_IP = 'localhost'
BROKER_EP = [BROKER1_IP]
TOPIC = [ "motorway_cameras","toll_bridge_cameras", "probe_vehicles", "inductive_loops"]
EARTH_EQUATORIAL_RADIUS = 6378137.0
EARTH_EQUATORIAL_METERS_PER_DEGREE = math.pi * EARTH_EQUATORIAL_RADIUS / 180  # 111319.49079327358


CAMERA_LOOKUP = {"M50(S) After J9 (N7)":
                {
                    "coordinates": "53.31353873270574,-6.363575673942173",
                    "northEdges": "345616204#1.655",
                    "southEdges": "75259388-AddedOffRampEdge",
                    "partition": int(0)
                },
                "M50(S) At J9 (N7)":
                {
                    "coordinates": "53.32105761034455,-6.3702774491561724",
                    "northEdges": "4937552#1-AddedOnRampEdge,22941416,4937552",
                    "southEdges": "gneE0,11955830",
                    "partition": int(1)
                },
                "M50(S) 1.4km Before J9 (N7)":
                {
                    "coordinates": "53.33335994735108,-6.382773162408997",
                    "northEdges": "360361373.981",
                    "southEdges": "48290550.1878",
                    "partition": int(2)
                 },
                "M50(N) 0.6km Before J7 (N4)":
                {
                    "coordinates": "53.34727008589719,-6.386567333598459",
                    "northEdges": "360361373.2643",
                    "southEdges": "48290550",
                    "partition": int(3)
                },
                "M50(N) Before J7 (N4)":
                {
                    "coordinates": "53.35269470355068,-6.38544365135953",
                    "northEdges": "492226831,4414080#0.187",
                    "southEdges": "61047111,492229071,gneJ14,61047111.165",
                    "partition": int(4)
                },
                "M50(S) At J7 (N4)":
                {
                    "coordinates": "53.35885146892749,-6.3834896661669625",
                    "northEdges": "4414080#0.756.47,71324924,4414080#1-AddedOnRampEdge",
                    "southEdges": "16403446,4402297",
                    "partition": int(5)
                },
                "M50(S) Before West Link":
                {
                    "coordinates": "53.363722242995145,-6.382086740810554",
                    "northEdges": "4414080#1-AddedOnRampEdge.343",
                    "southEdges": "106130759.2098",
                    "partition": int(6)
                },
                "M50(S) Before ORT Gantry":
                {
                    "coordinates": "53.37334705444544,-6.373142233357861" ,
                    "northEdges": "gneE7,gneE6",
                    "southEdges": "106130759.791",
                    "partition": int(7)
                }
}


TOLL_BRIDGE = {
    "coordinates": "53.3617409,-6.3829509" ,
    "northEdges": "4414080#1-AddedOnRampEdge.343",
    "southEdges": "106130759.2098",
}


M50_Northbound = [
        "M50_Northbound-1",
        "M50_Northbound-2",
        "M50_Northbound-3",
        "M50_Northbound-4"
        ]

M50_Southbound = [
        "M50_Southbound-1",
        "M50_Southbound-2",
        "M50_Southbound-3",
        "M50_Southbound-4"
        ]