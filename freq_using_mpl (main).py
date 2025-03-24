#mic voice visualiser

import syncedlyrics
import numpy as np
import threading
import pyaudio
import struct
import math
import time
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patheffects as pe

max_frequency_levels = [4972.262564193408, 4356.980462973123, 2303.436949216465, 1510.538546695035, 1403.5873836520334, 1346.733843334883, 1318.4573982672612, 1304.1958185127705, 1279.279227025311, 1282.896898657772, 1286.8068707608545, 1264.3933972307145, 1225.9394019250665, 1266.5718851123347, 1262.7806843432695, 1261.719339874357, 1253.4407742254693, 1238.53227046595, 1264.6461351352832, 1260.4653418072455, 1230.3602280648122, 1236.4599567707241, 1221.1453786389798, 1201.3723932946666, 1176.9672421203986, 1257.351119305153, 1251.6696551054536, 1234.5056927865544, 1243.5773138841728, 1203.5826998624634, 1222.878123534165, 1233.1505153237424, 1181.8089845795146, 1239.0588512217455, 1141.8429662698347, 1220.9470620516188, 1212.2963966144118, 1192.3009804149901, 1161.8547829172128, 1025.9141741711028, 1141.8470231064466, 1115.1613679256436, 1107.4483261136008, 1115.797748501501, 1034.5381752066016, 1023.8767237235112, 1002.2583459751285, 1028.6179427205043, 1117.386077302688, 1056.9513143676293, 1153.203612194463, 1152.7173353484136, 1106.5411988127616, 1113.6742008089802, 1006.159008266903, 920.900035361284, 1071.7613521989756, 1067.7440190581012, 887.7840290528029, 1009.7586342123029, 1107.5461911212024, 1005.2827213931224, 833.7187040832397, 1088.9640013178475, 968.4586242832138, 844.4735557555609, 1067.039077647502, 601.6519875603599, 929.3675482116186, 623.3082405760634, 1051.0549457992693, 922.2404269966929, 839.6142960398079, 1040.6022685168982, 548.1745327879647, 1035.766881271167, 851.1149500687364, 894.2377349752381, 749.4633695873465, 954.1083783788735, 858.252902000961, 876.9133876011856, 974.3629731304103, 652.4673246705736, 995.0084165930659, 596.9882720874556, 984.7313442609072, 446.8777708999795, 990.1505509173521, 560.1268072436202, 966.6112282955561, 586.904661536826, 965.6283112568394, 396.28759905124264, 967.8230777576787, 616.6640885398918, 900.5486469783922, 744.4400034978287, 888.0088689036041, 751.9479237510416, 846.918357535545, 775.544157093014, 653.1485656791235, 935.0514687114636, 536.9796436051612, 945.0944263968734, 430.08469246882873, 948.7286392971105, 571.8652911496363, 577.0212686072645, 943.0198981421182, 396.30185725746543, 841.4560356971854, 767.7343030773413, 447.39005033854727, 935.9233628037833, 509.00961361587997, 671.0003775261902, 900.8426380860807, 304.8053189909742, 816.3468077775947, 784.7145696470703, 170.1442392682374, 392.2348719654718, 924.5210819596623, 569.0821260632858, 467.2165316873469, 936.9826528356439, 493.76450784827057, 696.9144273288256, 880.4594410020223, 279.76905965332475, 845.1680090303339, 738.8424666291306, 195.52965091381947, 807.5153294520651, 789.7561325273855, 181.61400166028454, 715.2677675790156, 852.7757600917115, 339.45449009968723, 893.7789071459741, 613.2815484944855, 189.05783256120043, 785.5819203421211, 787.0004059809522, 190.57210496865673, 343.21971251313823, 894.5128654952019, 614.9850499915625, 98.63736079443638, 465.78834688239624, 912.6391449523353, 481.56106269753553, 173.16361253667407, 750.6923434250823, 801.1489630976375, 215.17291916752683, 180.0132682146346, 757.384255388864, 797.5101815694369, 211.5533393486023, 324.189049191617, 885.7698726574959, 649.5151565508212, 134.81094197365127, 683.7707460321063, 854.0790424481124, 282.98386937059416, 174.40715130003238, 749.4223367578131, 809.0843423976623, 226.79658405465588, 394.5155081595161, 901.3990412027536, 562.3649740782593, 92.89526085950493, 361.69398788287066, 890.2121073528566, 596.038852032022, 106.3786162814021, 533.8049313093933, 909.323806581236, 429.68137447076674, 131.22941674392334, 652.1503363219394, 866.6399098898131, 314.86719788609304, 57.98269800632867, 208.6852794171492, 772.4836034974545, 765.0955584388232, 203.0173173794527, 95.1180392770365, 530.1832757913018, 908.5466998678039, 439.66910766431624, 156.1383696677408, 320.04086119055387, 729.4067380361391, 726.4483461872674, 261.91521936649804, 58.95812460490013, 40.84767810069277, 204.33736021593714, 763.6849207872712, 793.8759919503573, 230.86158617748012, 120.24751900259155, 585.255797498781, 882.2953814286321, 380.59134777083756, 77.10100496389495, 352.87067025195546, 878.123398887424, 626.0683601732951, 134.04216738786576, 32.8449238171215, 147.7896403352137, 652.05296448106, 856.7100343544399, 324.5753657182767, 69.70835480398833, 306.75602966936964, 847.8065735357384, 683.1107629695061, 167.32580619442734, 32.909894916938235, 92.97221697198876, 438.7367051521565, 891.2344899452931, 531.7836734338354, 114.09727648059825, 291.81135778688343, 829.5857198264407, 696.2647128520364, 178.47490280706597, 37.872450600823484, 63.55955163033707, 285.87232714296005, 824.2220383633803, 703.0856960833676, 186.18028616424326, 140.47531702045586, 585.5426453836865, 872.567752119897, 388.39898926244825, 87.83183722460173, 48.649487746983255, 224.92508104190932, 756.8185242520104, 791.0434070133086, 254.0644663124156, 57.460882305238506, 151.48093718329656, 613.615361802582, 857.3351149956274, 364.76242894686794, 81.91417527551668, 41.377875377424786, 166.81319616626124, 638.6297007616517, 848.752668507202, 349.22416301614396, 82.10719754951329, 167.73788517551174, 628.6260582875266, 844.1428438855959, 298.29976178193766, 98.46839724677218, 34.4995008881892, 155.88826967450106, 603.7425249402164, 870.466572751437, 393.7028359885349, 96.32020119428843, 23.184085629114897, 35.923838438293785, 157.62053711234645, 595.356539676975, 859.5825018811972, 390.57819647224505, 97.97133468078131, 28.776241055383895, 33.2024273108144, 124.05037417132243, 496.3691278836573, 876.0813737873356, 492.691380161844, 128.98192665979414, 62.7987767601802, 260.29818296868774, 765.2375753360803, 730.5202448043844, 156.15435607184205, 96.95135117561513, 38.07339457192253, 38.60524380683688, 164.18738012457024, 588.6225983722654, 852.520055898927, 402.9579641287801, 104.20588751871458, 25.99542038800447, 16.699496444986504, 63.47258374370248, 256.1419936642192, 741.6814619770114, 758.3133881153333, 271.6234133670744, 65.9682092872169, 19.34095073595587, 25.15934082044064, 77.70422489192012, 296.48777993945055, 783.5286383366424, 708.1156465802605, 233.58669607971723, 59.33480994230442, 17.220882123879914, 18.999384526974318, 69.17538437586872, 271.0995057341234, 744.5298318493604, 744.4732048801718, 267.36729784143483, 69.10033091408522, 23.977013549637768, 27.103325852101943, 48.35249532751943, 188.26605499429687, 613.6020533996507, 844.183664801971, 400.56970556690476, 113.04740787830004, 30.361151965416965, 26.790211996682192, 169.40444138030725, 582.0652548978868, 843.4360733275813, 402.18978435765945, 112.29125652402492, 28.83225229434697, 39.711763748784854, 29.3231531921037, 86.19680366169362, 304.09526852372517, 765.580865895541, 714.7166610538942, 260.3168576998958, 65.9844463579648, 22.83437225719118, 57.51383557524639, 219.44756619569108, 648.080034308043, 812.7282827143542, 368.73130648472113, 109.37463629496978, 28.34108723418495, 38.255153072759484, 133.48627222382328, 441.51115962926724, 840.3224786653005, 577.6771158973852, 189.65982754180916, 48.275624821682754, 19.161718189467067, 61.48629520905409, 232.8405794731942, 652.0223989792613, 818.7978242381153, 383.66435446251705, 115.4843926242501, 31.772142934927864, 10.001422001244658, 29.906285167244558, 109.751667048822, 356.26499141338735, 791.0513950657288, 668.8114403323051, 249.60372774902427, 68.95162651197222, 18.213744616039026, 36.057632020529745, 122.67700209759676, 398.49879805269217, 813.2028934529781, 634.8066287952084, 231.60731533787592, 62.30742901139777, 16.534508779067423, 7.430505465245485, 10.371962835949883, 41.46792434210955, 142.71902513227138, 441.14298881604276, 829.6203651632001, 596.630812567708, 212.69814034494428, 57.19497394853264, 17.44549367313103, 10.98239357567925, 30.85776067063952, 110.36924980285231, 350.8909365877285, 767.0256040205212, 689.666252154052, 275.7080249646723, 82.18038499201127, 22.352531280793396, 16.413269913145573, 64.06164496878763, 207.20713465250662, 578.1499341733727, 823.0671012361332, 463.1364395565475, 159.0533179986434, 45.413600933771455, 16.537545961722422, 17.86998602571273, 18.734151580818633, 31.975992176807722, 96.40610420734883, 328.9848122679087, 735.0453406411222, 729.3597259469234, 321.5026088909027, 101.94852341894351, 30.127361134202925, 81.49010446766263, 311.7817986180839, 741.4586535867359, 737.4888160510209, 255.69432811123625, 125.11428736171557, 26.870299086964692, 26.617075884910438, 26.116449026326226, 21.100111504929576, 32.669655682807175, 113.44138259005949, 336.49648710867007, 730.8336718665023, 708.2420100363453, 309.5243029722135, 100.00713734017135, 27.973575441502614, 11.51160612968265, 26.085278577816798, 81.3044693492723, 263.92698158840676, 643.846334379747, 784.7584901339454, 411.0285983632195, 142.89649875275578, 43.48139239676228, 14.049374816494078, 6.380716357721457, 14.744880407431003, 47.45591964766439, 154.8443844982247, 426.67034556769954, 777.1824778547694, 624.0548456624331, 264.4586933968323, 88.55382572070334, 25.74381214650442, 9.98675002565958, 17.339314226709313, 63.17737167543478, 229.9856857082842, 566.9831304656052, 809.4966349283418, 506.86304012159815, 191.52644958809043, 58.0033568936272, 18.91852828503702, 22.121013883968857, 94.9794282078922, 286.71345876986254, 654.4822574592534, 774.7047730760056, 415.65468628989663, 149.88636249894472, 47.291387091883, 15.987893745523923, 6.533363638873557, 5.849551225565239, 5.994957066641559, 19.930327362633374, 67.15568663994674, 205.12530283424277, 519.6667830719308, 794.4070495195587, 545.5118528213527, 226.67190286193295, 71.77983483805855, 20.995723712621743, 10.361452342053274, 13.463204086679061, 45.153973086443386, 150.4774427315129, 399.8621146535007, 739.5176175604793, 661.7374149306453, 314.557779757035, 105.71483462020419, 32.05529488585193, 11.73519328268504, 11.71518134655861, 24.77983051227589, 82.20058788488495, 249.18926865149152, 576.2676589274402, 784.401227625577, 496.46377438264284, 202.7407936770852, 67.85486563432866, 21.407050114736577, 19.915893780862408, 23.621510882222122, 27.73323054771346, 131.82014272804778, 319.80206680735245, 660.6081304049237, 721.3604257962, 415.210141811452, 176.64028979540848, 86.52499213919013, 85.55045149503886, 85.65024016830469, 62.686381847175525, 68.96228170889006, 92.99500280325961, 283.00264005331366, 589.6364477302051, 773.1833923767135, 422.6401202332479, 189.5954447431459, 59.86067964814269, 50.06888498186801, 42.31283422125697, 28.718000444366318, 23.90130840403441, 17.051389553702244, 18.410533398743674, 16.976547272828007, 18.6680506799879, 32.09075095513468, 85.7364993932014, 264.42198684867463, 568.7669387702873, 742.4376567498805, 493.99771121556785, 218.5363223710364, 77.5528698448196, 22.28377888802002, 10.686623228117105, 14.290795109891791, 12.785730368198351, 62.63485939984469, 141.9506802231739, 383.6359843454364, 691.7133933749144, 692.6450188806782, 377.98218391411996, 132.35279511319033, 54.51079658624749, 19.58381190800279, 8.887494177236775, 14.127987975360037, 24.485810255617043, 61.38909981763511, 195.2159801807564, 453.1268452782488, 729.8040463510266, 627.3939802240686, 322.5005497915872, 127.28734734510137, 30.01759435555384, 23.60964619702505, 17.3178444986675, 12.1914333956081, 39.67809981038251, 44.328694407172, 173.85375771951644, 445.6621423434579, 719.0472576640012, 630.5190865767339, 326.5122641338852, 114.84494800628083, 47.25846018907651, 10.732060314917561, 9.595448305292832, 9.15605151773404, 7.1820889110503, 15.092938092710806, 12.816569122046316, 29.058778619614102, 43.58646061845334, 163.6672817155335, 435.2201236430107, 717.4848463717133, 651.5979502861637, 334.3738529375579, 158.75307985163573, 35.4334766754253, 40.87611590439013, 21.800135358885868, 15.011910252833557, 14.504402105302784, 38.84493281846979, 86.04814273303357, 257.54116696838923, 544.8609932670811, 739.4344159057252, 542.6893793852241, 259.8558260735091, 105.86802080279969, 37.62366387596509, 7.906220126866139, 14.219531019041257, 24.805317706624038, 13.535942637214296, 44.20352817359335, 129.59693747931684, 306.51868378305244, 576.0010333794553, 724.2804436930842, 505.61684664917414, 250.4307349625939, 95.30366678963843, 15.04916762870805, 30.570581178838708, 12.54284114053545, 13.159416243953737, 33.84468533330399, 33.63596588236917, 101.6795432640492, 263.6058797355244, 535.798763311637, 718.4373837251428, 555.704946759292, 274.49079501769654, 112.2988591870231, 34.16905422961588, 19.118744220039336, 11.67592541270379, 9.357034673365419, 10.594541055522582, 10.621008502502326, 11.95845961483882, 44.878637480877345, 105.91540366843465, 293.701942268095, 554.76564561584, 716.5712283700742, 537.7548860279238, 270.8358463458536, 103.03848559954885, 24.078301600148713, 34.16118660395022, 18.804142875259295, 29.836240164295425, 27.215661272000688, 29.186283029323832, 20.67961236294946, 6.285710460707027, 16.73587376266448, 56.45937222748836, 136.91688768179034, 340.6483235497044, 597.2528322513095, 683.7232856757954, 471.3964380665377, 215.31861206520514, 72.07525948448513, 41.32243864021975, 15.55333138383008, 9.14455783259705, 7.81599676786448, 13.761545292439308, 18.30572955764899, 20.15005549015052, 13.0510468236556, 15.393464809340417, 37.31340778269715, 104.9869289200198, 263.62724239934363, 506.49000544042, 682.9712208023155, 539.8757357681133, 265.7268446634466, 124.95314422455637, 40.37312794814905, 46.44769371092393, 42.62433253860356, 30.123920181673167, 19.00044372381449, 24.705989164287477, 25.1359921339196, 18.335787112421226, 22.24677034753763, 105.31739364773873, 250.51377959899534, 454.9202514988773, 592.4598986333526, 492.76949481913675, 284.31410611991095, 113.36113212392311, 59.07719779483719, 69.04198783002163, 69.24899720421071, 63.54717318832748, 66.22908929924478, 53.888360606133574, 39.55210218498785, 31.84885516036165, 49.945454159808875, 65.52805072186736, 122.04320596267435, 261.8159516093828, 447.15707134721555, 533.5246905719926, 316.0381777678969, 161.70424990886653, 48.573543669428126, 49.63889197153704, 12.637458053176253, 14.81847769990013, 18.904540759602437, 10.817069268406337, 17.616253378329226, 14.123866714729303, 49.399216375446386, 117.53011339828687, 235.8862526023122, 367.94632458348445, 389.53020407084097, 272.72271831428645, 146.46416197207702, 66.21953862000183, 16.09314759299739, 19.346842442147654, 8.926809350771448, 14.078867887780394, 17.4126251159953, 9.854087992611314, 5.289228653003073, 17.3479797864, 28.63377990741612, 23.06250259775879, 77.71068505567584, 134.88550589714748, 251.7276559376178, 295.75012677490935, 226.65274087952236, 110.4165260845533, 58.52616018903617, 5.035924245157103, 13.130900332184046, 10.862885028405781, 4.288335082309138, 3.824001493171133, 3.749782568647399, 3.3525939637438307, 3.8869447524534007, 3.0962835172091236, 15.22908384012873, 27.65759391569173, 60.17249716063229, 123.9246736510023, 163.4563075475814, 151.15465638738016, 102.44276397574819, 54.30955969251061, 24.541309062470138, 9.981294634664742, 9.458320241381182, 10.794728654093605, 9.160685614838254, 15.277925534313942, 26.970344035484118, 54.19604607005272, 87.87262816870309, 106.75400315448135, 82.59232277081334, 49.57122824756031, 24.612388065193866, 4.564457339543795, 3.0454386041464296, 3.749099521859617, 3.582111736881068, 4.767310404673267, 3.0468830407941043, 3.0141810064428864, 3.0318723298601973, 3.013891021823697, 3.046140189569942, 3.035826544398378, 3.003519390957071, 3.565723565088749, 7.929158852634746, 18.08656992219968, 29.21415148678901, 33.22381670469672, 27.807783568594168, 16.9582816697685, 8.390040496657624, 4.018416584252074, 2.998882731446331, 2.9959731331459745, 3.005989862807156, 2.9871351224884655, 3.0090014575975736, 2.992216180165952, 3.0082978501463926, 2.9962636650827448, 2.994055225668946, 2.978001835722578, 5.141302070151071, 8.007815700648854, 7.975853350497371, 6.241955162935959, 1000.038489935963221, 3.0061789572046718, 2.9719843723895316, 2.9923867513339295, 2.963388333406855, 2.9636024766377203, 3.0113274648351376, 2.984220217987199, 2.958851626174212, 2.9816064142290024, 2.974358874347422, 2.9643318031717234, 2.9785525536485347, 2.967409260276818, 2.9878198407685073, 2.9696086490384275, 2.9616409322920485, 2.9631361208936826, 2.9699349158043082, 2.9657124457349946, 2.9481766699473915, 2.9566899668282316, 2.9623837550307623, 2.971274419554574, 2.9506307694707803, 2.9473453624459216, 2.9394831945618316, 2.964484303737842, 2.959075634291878, 2.9529139805043485, 2.9353220362502226, 2.9652861971920936, 2.944882448974996, 2.949894201360155, 2.9489987019557065, 2.951181893824965, 2.9441751962986373, 2.9420594107369884, 2.945736480072458, 2.9442632040882466, 2.9399549753964296, 2.9212522167915838, 2.926063722494988, 2.928180814246174, 2.9380347027005755, 2.9417242993209607, 2.928314025443748, 2.934634981662709, 2.9172803501495417, 2.91372856180268, 2.9228774209163535, 2.922955273731951, 2.9297264948451396, 2.923528225935785, 2.9130181550197394, 2.9226406864214365, 2.9080188975752455, 2.9083209648777935, 2.9240472769526384, 2.916940444994676, 2.9152207212524397, 2.9082906157868442, 2.9226593304349904, 2.899168286936949, 2.913510827163281, 2.913731957438199, 2.9335194051826208, 2.904951366250543, 2.8945599449269745, 2.9093687170696176, 2.920466764972544, 2.911181139551715, 2.8932865621805255, 2.914033431128267, 2.916428257590901, 2.889302620404295, 2.890902416481674, 2.905324135609992, 2.9142626058496837, 2.89172176177473, 2.9057215755171395, 2.8801717037367913, 2.8971511491636734, 2.8937439345870395, 2.904806336546134, 2.91202599466582, 2.897280023716409, 2.885063625749367, 2.892327352087607, 2.8995650065521015, 2.8653851233362126, 2.8881604525164906, 2.8943135681355536, 2.8880370508791167, 2.8888721277368483, 2.885872718436325, 2.8922584995290532, 2.903330925677144, 2.881964126341265, 2.8842532330122563, 2.8805594721729273, 2.8841122295784207, 2.8735443820036592, 2.880362264869356, 2.901127482658322, 2.8736960993636314, 2.8632996021577837, 2.8868537840077058, 2.878859263251125, 2.8620975898332692, 2.8671031940185583, 2.8766071361520034, 2.8797792793030697, 2.8841466045055393, 2.8678932925752054, 2.8685073909974843, 2.8676543815356936, 2.8756650345622266, 2.8703166832299423, 2.887773270670868, 2.8768635455047367, 2.8639497254379367, 2.865911273165676, 2.8782931803759766, 2.8702460372189442, 2.8771698407922757, 2.8679185205950177, 2.854488230431165, 2.890051212047838, 2.863282766817322, 2.859171801043498, 2.8723824427585507, 2.869870710724042, 2.857840816627645, 2.856705489983132, 2.854874899849243, 2.861728811290825, 2.851890518808856, 2.8673240188407814, 2.8806833011638457, 2.8507175082282763, 2.8508618822951326, 2.8651682260235165, 2.859930237120357, 2.8580347309192633, 2.8665694941998483, 2.8371591406617727, 2.8614002126289044, 2.8528007320665085, 2.8551222121266333, 2.8484971352137145, 2.8524521350128214, 2.8650831984201406, 2.8712227643540715, 2.8557018171625823, 2.8528180676086965, 2.8461273654365153, 2.8459472517535427, 2.8475450536916878, 2.8616976848836875, 2.842610788369641, 2.860713154716029, 2.8544739341773018, 2.851232386573414, 2.839590990081699, 2.8609567863864567, 2.843860732825336, 2.8502602149483547, 2.863747842909222, 2.864055707295215, 2.855717219942337, 2.853654311345548, 2.8403453103312963, 2.8427980476825385, 2.8522672494698593, 2.8606077552992506, 2.838500770691829, 2.8362560938006904, 2.8508514068959303, 2.8433342365965277, 2.8384405480858135, 2.8558996672629653, 2.8408704729818988, 2.8467138858080707, 2.850736116613893, 2.853129897196384, 2.8557168775199946, 2.8391743976096944, 2.8387921360385393, 2.8575167399621235, 2.852745195750573, 2.844259726491257, 2.859291584367649, 2.8440470228152805, 2.8425386161889916, 2.845546204621149, 2.860182487591536, 2.8598418793812406, 2.842475634930493, 2.8745474264939723, 2.8272466297626124]


#========audio stuff=====================================================================================
# constants for the audio stream
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 48000                 # samples per second

p = pyaudio.PyAudio()

# get list of availble inputs
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print ("input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

# select input
audio_input = input("\n\nSelect input by Device id: ")

# stream object to get data from microphone
stream = p.open(
    input_device_index=int(audio_input),
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

print('stream started')
#=======================================================================================================



#========mpl stuff=====================================================================================
def truncate_colormap(cmap, min_val=0.0, max_val=1.0, n=100):
    """
    Truncate the color map according to the min_val and max_val from the
    original color map.
    """
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=min_val, b=max_val),
        cmap(np.linspace(min_val, max_val, n)))
    return new_cmap

def colormap():
    return colors.LinearSegmentedColormap.from_list("lime_to_red", ["lime", "red"])

def split_freq(freq, indices, prev_indices): # splits given sound frequencies into groups of frequencies
    freq_ranges = []
    for index, prev_index in zip(indices, prev_indices):
        if index != prev_index:
            average_data = sum(freq[prev_index:index])/(index-prev_index)
            average_max = sum(max_frequency_levels[prev_index:index])/(index-prev_index)
        else:
            average_data = freq[index]
            average_max = max_frequency_levels[index]
        percentage = average_data/average_max * 150
        freq_ranges.append(percentage if percentage < 100 else 100)
        # freq_ranges.append(average_data/3)
    return freq_ranges

def update_text(list, string, string2=None, x=CHUNK, y=0, fontsize=20, color='white', zorder=0, ha='center', va='center', path_effects=None, wrap=True, weight='bold', has_korean=False):
    if has_korean:
        font='Happiness Sans'
    else:
        font='Dengxian'
    while list:
        list.pop().remove()
    list.append(ax.text(x, y, string, fontsize=fontsize, color=color, zorder=zorder, ha=ha, va=va, font=font, path_effects=path_effects, wrap=wrap, weight=weight))
    if string2:
        list.append(ax.text(x, y-5, string2, fontsize=fontsize-10, color=color, zorder=zorder, ha=ha, va=va, font=font, path_effects=path_effects, wrap=wrap, weight=weight))

def update_bars(x, w, max_y, height):
    c_map = truncate_colormap(colormap(), min_val=0,
                                max_val=height/max_y)
    img = ax.imshow(grad, extent=[x, x+w, height, 0], aspect="auto",
        cmap=c_map, zorder=1)
    gradient_images.append(img)

#remove toolbar
mpl.rcParams['toolbar'] = 'None'

# matplotlib.use('TkAgg')
plt.style.use('dark_background')

# create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))
plt.axis('off')

# variables for plotting
number_of_bars = 32
x = np.arange(50, 2 * CHUNK, 128)
w = 100
max_y = 100
gradient_images = [] 
smallest_freq = 20
multiplier = math.log10(1024)/(math.log10(smallest_freq))  #1024 is the length of y_fft, shouldnt change
indices = [int(smallest_freq**(1+(multiplier-1)/number_of_bars*(i+1))) for i in range(number_of_bars)] # list of indices for frequency data for bar graphs, start at 32hz instead of 0hz
prev_indices = [int(smallest_freq**(1+(multiplier-1)/number_of_bars*(i))) for i in range(number_of_bars)]
prev_data = [0 for i in range(number_of_bars)]

# create a rectobject with random data
rects = ax.bar(x, [0 for i in range(number_of_bars)], width=w, color='blue')
horizontal_rects = ax.barh([i for i in range(5,100,5)], 10000, height=1, color='black', zorder=3)

# basic formatting for the axes
ax.set_ylim(0, max_y)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0,max_y])

# show the plot
plt.show(block=False)

grad = np.atleast_2d(np.linspace(0, 1, 20)).T

# prev_list = None
# def compare_lists(list1, list2):
#     # Ensure both lists are the same length
#     if len(list1) != len(list2):
#         raise ValueError("Both lists must be of the same length.")
    
#     # Compare each pair of values and take the larger one
#     return [max(a, b) for a, b in zip(list1, list2)]
#=======================================================================================================



#======spotify stuff======================================================================================================
clientID = '6dfda82b74cf4b0f8df51c4db23cd6d8'
clientSecret = '9e59d4d904a740889376ef247ae34010'
redirectURI = 'https://localhost:8080/'
scope = "user-read-currently-playing"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI, scope=scope))

def parse_lyrics(lyrics_data):
    parsed_lyrics = []
    lines = lyrics_data.splitlines()
    for line in lines:
        match = re.match(r"\[(\d+):(\d+\.\d+)\] (.+)", line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            lyrics = match.group(3)
            timestamp_ms = minutes * 60000 + seconds * 1000
            parsed_lyrics.append((timestamp_ms, lyrics))
    return parsed_lyrics

def get_lyrics_at_time(parsed_lyrics, time):
    previous_lyrics = None
    for timestamp_ms, lyrics in parsed_lyrics:
        if time < timestamp_ms:
            return previous_lyrics
        previous_lyrics = lyrics
    
    return previous_lyrics 

def detect_korean(text):
    korean_pattern = r'[\uac00-\ud7a3]'  # Hangul syllabic block
    korean_matches = re.search(korean_pattern, text)

    # Check if korean is present
    has_korean = bool(korean_matches)

    return has_korean

song_title = []
song_lyrics = []

def song_stuff():
    oldTrack = None
    prev_time = time.time()
    parsed_lyrics = None
    prev_lyrics = None

    while True:
        time.sleep(0.8)
        current_time = time.time()
        if current_time - prev_time > 1:
            currentTrack = spotify.currently_playing()
            item = currentTrack['item'] if currentTrack else None
            if item:
                track = currentTrack['item']['name']
                artist = currentTrack['item']['artists'][0]['name']
                if parsed_lyrics:
                    song_progress = currentTrack['progress_ms']
                    lyrics = get_lyrics_at_time(parsed_lyrics, song_progress)
                    if lyrics != prev_lyrics and lyrics:
                        update_text(song_lyrics, lyrics.upper(), x=CHUNK, y=max_y//2, fontsize=100, zorder=3, color=(0.8,0.8,0.8,0.6), path_effects=[pe.withStroke(linewidth=10, foreground=(0,0,0,0))], has_korean=has_korean)
                        prev_lyrics = lyrics
                if track != oldTrack:
                    while song_lyrics:
                        song_lyrics.pop().remove()
                    while song_title:
                        song_title.pop().remove()
                    lyrics_and_time = syncedlyrics.search(f"{track} {artist}") 
                    has_korean = detect_korean(lyrics_and_time) if lyrics_and_time else False
                    if lyrics_and_time:
                        parsed_lyrics = parse_lyrics(lyrics_and_time)
                    else:
                        parsed_lyrics = None
                    update_text(song_title, track.upper(), artist.upper(), x=CHUNK, y=1, fontsize=30, zorder=2, path_effects=[pe.withStroke(linewidth=20, foreground=(0,0,0,0.5))], weight='bold',has_korean=has_korean)
                    oldTrack = track
                    
            else:
                while song_title:
                    song_title.pop().remove()
                while song_lyrics:
                    song_lyrics.pop().remove()
            prev_time = current_time

a = threading.Thread(target=song_stuff)
a.start()
# =======================================================================================================


while True:
    # time1 = time.time()
    time.sleep(0.01)
    # binary data
    data = stream.read(CHUNK, exception_on_overflow=False)

    # convert data to integers, make np array
    data_int = struct.unpack(str(CHUNK) + 'h', data)
    data_np = np.array(data_int, dtype='int16')
    data_np = data_np * np.hanning(len(data_np)) # smooth the FFT by windowing data

    y_fft = abs(np.fft.rfft(data_np)) / (CHUNK/2) # FFT
    # multiplier = math.log10(len(y_fft))/(math.log10(32))
    split_data = split_freq(y_fft, indices, prev_indices)
    # if prev_list is not None:
    #     prev_list = compare_lists(y_fft, prev_list)
    # else:
    #     prev_list = y_fft
    # file = open("max freq lvls (artificial).txt", "w")
    # file.write(str(prev_list))
    # file.close()

    while gradient_images:
        img = gradient_images.pop()
        img.remove()

    # update plot
    for i, bar in enumerate(rects):
        height = split_data[i]
        bar.set_facecolor("none") # set the color to transparent
        x, _ = bar.get_xy()  # get the corners
        current_height = bar.get_height()

        # print(height, current_height)
        if height < 5 and current_height < 5:
            bar.set_height(1)
            update_bars(x, w, max_y, 1)
        elif current_height - height >= 4 and current_height >= 5:
            height = current_height - 4
            bar.set_height(height)
            update_bars(x, w, max_y, height)
        elif height - current_height > -4:
            bar.set_height(height)
            update_bars(x, w, max_y, height)

    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        pass

    # time2 = time.time()
    # print(time2-time1)
    
    