from telebot import types
import time
import telebot
import traceback
import config
import requests
import urllib
import json
import logging
import copy

bot = telebot.TeleBot(config.token_bot)

bot.send_message(config.myid, '✅ Бот запущен')

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatstr)

fh = logging.FileHandler('/home/tgbot/mentionsbot/log.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

def start():
    try:
        f=0
        month={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        cookies=[['2ad9c81426158a563b4ec211ab8f06b1a9746761', '66a566e8f480a0b5bd9ddbf7c5c0c4e710a6749de74f36eb2601c007ab5558906150fd1bd6b49c5108f05384950845f5265c4317c79b5dc1f30d6219de778c4c3dc98211b1e0067d2b6a387c254640a0'], ['e0015d0f238a38657a86ea5d548ec3fb514afe65', '5f068d37d14c6ae91efc58876e5120469cac384a4d293f60b061884d337f17b9d767d1b5cdc5329f7435981603fcb08bc662fa0e9da80ba9e5edff780720454000ecc592c53e15b9bd63e60accacebdd'], ['1ef9aedfd06957726d25267a657878e3c5022a58', '4aec3744783d4469d03b822c781decf5989ca07f1216691466c875c1cc39eff427d3a01e98d93b4c499e15f6377d5f70beea8cdcaa69683b0d2270adcc993e0ab06468ceb3e7b927e08b4e47583bfd5b'], ['b6970e0f4c8f55dfc81757845f7615226257ff4a', '63c38b59ede109f1928870b081fb572fbaa8980c89a579e008b94a38f5364a5de804ef4d8f2cbfd34507e5b06bfe0bdc32b54b18cb1973d922cbd7cae990b0893b4799f182778b652b9cfa58ecaa5999'], ['984cd5bfab2634a4d978ee5410181f605397b691', '1e49a22e2c45a223313dadcfbed392a883890b7487d15f48e9b42ff66ba4c65e7b071f389f33603cc7577a2776e9496ba2d010cf2ab39a595cb480a0cf7665280a012c21c2899192f83b8fca603c3e59'], ['ebc13f94f09656a934748ab5339f0a6a917026e9', '43473bc1f8318ec9bf7cc0a1469659028feeaabbc8d48e42a7d352d623657d551109c421718cc43315906d6d1239dee67b70e92733c5f279a5cfa948743f9d18828cc18265f42ce3b7c099ee2a19d963'], ['76811854db5dc21b28b1f7ede1c49071dc0775a4', 'a626e4a0c0a3ad4163300bae1115a5ad162b2222acdef55d277e98094c298d78210b67c0e41e36a122e3417c7f9dd29ae39c0652471e60ae0cd3f52da66bf8924c91c4fcda75e9c585e2437650fb32a2'], ['36dc6134897dac804bc6dd28118c688f343c3539', '081897a0e221cac57a1cdeff6def903fa4da49c1737baa7393aa4e2ff986a88dcde19d9398fa91fd43885f5202819c4f3b5377bfe82796854b87d0b8aecf125b6c97adb567dce4f35905c4b271da874d'], ['ddaf61f849045a5e4639e69f4ab7b9e97cdcd50b', 'c941b7c5c94e1b40b510bd7879604da91a9ca12928c4bd40a0fff46ec5fc9d0347ebebe3feeeb4f527ffadb5643581140c41754bdd5478ab8bfd23bca8eede5b66cb96675efc3458d4e91b381d1f71f2'], ['2ccca56bc59abdd0910d368d57ae7654df26213e', 'f0258319d4dbaee51764d5611d30b99b596a1a85d32892db8fc35abdb01043b7bc7010656d0e898ac0d57db6dc4a768d549447592cb7caefc033b8d835763b82539a7542057dea62304253c34e9bb76d'], ['da541fef4c9da0f49166e259a082ba4098b694eb', '4a61990e1bcf2982abd487622ecb2bb11806128cb895233be63e450e432b9fe98e0f58d230c7a931363e1af6a0395578269d0f6018e0b1473714463e5c441402f9fc5d3796effb9a47f9a783680aea6b'], ['150008550e30f07313e6aa461f121b9f8ecccd4a', 'f72735898c8312e190cf494747da9cf3d667584556fe5f4fb26b0809f41989ade150ada67dc703faaa4f46dbc2122a40096a52a16f64e962ff93abc41a72500dce452956b5458752468b6d6b98d71f51'], ['5eb6d8058946024c59d8549c93d0b471e0eae3be', 'e9e7a1c8bd43149d94fc6be8624a6a9cacf72cfc504554702c7cb3ec2edf24fdbd307990fc03da685e24b40fae452b5375e756be6d20f5b8d1dbe257cb27ba1e0d69174d9d07b69fc5496a56afe0232d'], ['715fa1876d5222403a22f5d4300827be00653413', 'a6550e7dfd5c1770c14cc780e10a4e57ac739ac4f97239626243f6b136e9574654b094feeb8b4eff4a680d7095ff33c7d7d0fcf8317c7406cf1b573c2afa5f1cf0fce4909434a74ceb6540551ad7e899'], ['30ac532c9f0fa34a581896961e286c3b1adbc753', '52761068912367839131a9d65d8bf4f931e0f0d9d93048546bbe88536e963a249799e5fc844c024ef287fc3a8e46e46a9d403bb5e366fbdc6c200b03dc124311979cc4fdb472fe333306949922e1669b'], ['c52495034fbc2118c5ba550f807cbeb48b4eb9ef', '7b347f8793bae0e0c76904f7df4fb60ebdac09744c2e5756b8f8364bd11ac9f2dcc1f1e61def5fb52a979efb895d292e5d2cbf694eb3b95b2c97e2e24442ed1e113b613b966cf7e5eae47a316395af7e'], ['935ac206c9998ec6c966f44f1a2624faee3724fe', '349d115182ea3fcefb69a397d8fd43c9714371a38ce8babd8d0a99e9850c1c32a9ac0bc6e02354bdd911029bbd90739d800bde54458704fd924676c09c00fad177d77f48cea5d77aa1f507d3ac50399c'], ['089d1a9db3878fd73758acc7fd02e9dcd9a291e8', 'd796a5627d2f76dc50b5e0c7ab31e94083dea72fcec8f75f286e11624677dd4260a504f4a4eee07ebc7c263236de9a667ff012de7d2d5998d7e4fd4ab67f19daa7ffcc73cb62c9cff894a2605d3b2944'], ['7918e20ebe4a579a6d2a17a65d9eb457b60901a1', '4f61091b19c6375758218e5b71845fbfdfe91536b133f1056847ada1ebd9e87a137cc8f6364246904b822fe083ecd7dbcd574316a1c945899ee4d5f15611c32005e36481b0dd0a2cd7a614ae702118f9'], ['0eb799bd529bf1d778e792abca619ad5232ec485', 'd617e8c17f4c4be4b95334144f8a4bc6c032514c44cd0c07980c036ab2293b151d3c22f7688f85727ab66bbd59a758e2076b23bc369019b2ffc37fde5054e3b47ba00c2367390ec09d2518e56ee2c7ee'], ['3c0bb5007905dea0b18facfe6881f937a8de1f3b', '2065a309915c704ebd30f75e4da5a8a3925e78dc23838b8fe045f229491fb432e8406c8a814b0433b2ad3317e344832fe02867b72e6b2a82db249300f86d8165b66584cb27e9ed68429b7564cc0797d8'], ['6d6295a03628bd731c41dd7764b095afb7d516e4', '95c7fb7cccf6906d7ccecaa3ca2895bf5abbbd229a2987bef61b0cb929e304b4234c5d88a98024ca659ca3b41f0708ae5bbe6951badf471ab5c0446c2212982ef49f19b97a0d02cfe5ddb3f1d065abe5'], ['c799ec798b69d378a303340f8d172368dcb92ef2', '209caea0611c940506eb0a940d79a1e528aac35ec95cd93b2da1139869e9cbb3e88b81366f97a364456641e33e23e7ab1038659588831fa3210eb3df1be43d402a448eadec542ad824fad2cba33e7f4b'], ['c6add6c3f91adeef20a9a98dcf35f79096d83d6f', '6a0e8612d6ab889b56083bab6e83702246d6ed76451305d0e092ca16427146451f4eae4a063e45b1822bf0e25484fa13a39524dcda62a23dd742f3a08ae5e09244666626594f79cd34c621434d3d3d42'], ['863e898cb34a99b8abd3a4d09b1590a2d83ba192', '9d6c23874286d03a7f140581b63c53ee16818bf7bcec3165565751fe8fa4a22180787154aec7f66aa0f456b32f0d6a7c18a4709fc8833e31f4d29bd8a2469a0369a9d5e7a5a9b802fbf4c10e2e726b1c'], ['2aaab7af61efb8b87b8968373c295e8bddb9328c', '8baf9c104fc6fed80d54f9eb756eb983b664509c14a3039880b5daa0337479f7ae1b422f464e623a7c5a00a0c081b85f1c87bb0e72e406c1638ba67bca7ae399f9293a1dc64a4132ce7934963de8531e'], ['a1cbce4788bd1607547fd79f45b3cd86a8dcf417', '7ef61721bf771a64cf40565cddb9ca982c012fece5bfc5b14216efe6ec0ce185784a770d49fd5e2311e5fc2f7f9de45400748830b3c47987ee1c4674b1f3dedb5df0bf0282f16ffe910463ccd5bf033a'], ['b1446abac46c93beae78bc5c3ff93f2d68144dc8', '32d08f1d0f3d0478deca4b718706d130e217d786fcfe1f400cdeeb0a7c9c613e8c68a304f57021ad916fe81961e70ec2f117f3e06dd2aaef5c6bf7374d3f19f98881c62a3ea074ecfdd80bca40801f40'], ['6f00f146f9c6f30330bc4292785278d1bb3a4d90', '11562dd9a3e4b614cac587aa14a2de0e684872512e7fa5453292688463f73dc956b6938f74f5be95e29e1f1170bb46babfabd525d2786270f42c2c610792209aa7a98f80ce3778ba0bbcefca5c40079d'], ['43e9515258de7037235e6466a654f4447fdf7252', '5ca19f27f7241eb100469fb3344c8c7f4355e87e7d32a88a4c223500928da9b004f54920c974eacf895d14f85e051cf48487215fefeaa55ac133701a897bdbfcdc1fff6125b699206addba0b01b5a007'], ['86fbef6141a5ff253406a04f9fa1396f69f570e6', '3a2ac1ae235c7a1a803eafd6ec2646a685b5102ab07193341b35fa5041ab69e65c208109f83838e8cfa464cdd6c440aeffd8c2e03cd8d1bdb176c94e49653b5e5108b6ea68ea1afbbd81979f509029e9'], ['2040dbc2484084bcb36020bd72f0ef3064b55450', '2584a41e5eacf3b5dbaa0e2bd374d9fe93a2cd613b12822643f45e1f9a9024b2fb958c8229093c5a1e06d51cbdbe30c39338aaa678a8bed4baab3707c054b334b11158ce02f6b239d6e0a7d7da0a4cc0'], ['8b3a1f66d4ab1eec217ae78be0485d2d8b4b8e68', 'd5472d6e228d4bf98bb087a3df8ed1034a439d4392647271dba305d8bd779590f1c0523377984c5395342b6955c9ece88f31bf45ed6c2d75e85fb51440862a5c02d5e3acedc1d7277a200f0ba03c84d3'], ['adf62e9447ffb2fed01d352671cf396f9d2b578f', '5b8b7fb09a2267d2ac9b28afaaedbb81b674d88c5a9bfd5df48bb33d938c1a4331c464f49a38d74b78f272bee4c832fb809f675e52adb3731f212bde3bb945110ce54ae78218a031b0e2d66752035b18'], ['b21ccbc4d6a5006897a40bdd05496127e3bbfd64', 'd1c880c6e96d6b8e76b0f5259faf92c3de39fed882eef689a957864f136f6e02f32f029b966a50405a082344f3bba4d38bc7fca67686043406987359fdbf97ed55ce3c0ee2b49eba557441d81a8e7d26'], ['7e5f9e13f53299d20183f657c6f148ae83ed35c2', '5facc7db68411ddc0db018e977c4caf577eef45da6728cce40b800bd940bf67400b8f12487d4e0b7583e860e2529c6501f0fe3346eb1e9ee5d7ed16f97be05265fa6e2faf1739fc4512c699a6da79833'], ['96b92d36297ebab32ca7182180a0fe9439a8741b', '1435a3171f8b16f4ff815369e1ea74730b4a262074db443e196650e0e3528a031deebda6aa06e3252ee0f7b95f59d008619d2bbe63b6a6e917f01c4274c560f9f7e915cbdd59f0296907f61f980114a6'], ['80fbac1dfd3a2cd51c93f1e03eca00bb0477d400', '2e1ceba7739d9f44ca6da0f6d73059b164a212a88b58868781792c8079077c48623e4538f0d0befe65bd4b95d2594c82d0f81781db5ff3f5ce69875085ee4274f8dfcf0ab07ff57e93c7055a71f9ecbd'], ['757ed6dfb0d1106164bb34b1935fd2905f4810bc', '795a5b2985fbd5a4f294d490270ebf9eed5c67992f3a6e15801d63c88c3e7aa62ff8cc00cdbe6a079daf85c473b4567fe334cb409bd0781bdf0e81c35b0fe87faee60a604021750c808e5151a050c520'], ['c897672cba155544530f09100c7430136bff7de6', '5c7621226a0171e550b6e2eef3bb3a28fbf85dbfe8a61bea6d942a8138b01cb6a8fceb0871e789c510349d1c75ead1c133998873f07b7d0c6d97eb604ce2dff8534c2b4d4532b529cc21417796025ded'], ['49fd8bc838ce677ea5bf1cf0eb194296a4f47d22', '5d14d1e6f9f365a955feb4646a6839f417677f8e006d7027d5819ce76700e5a8a843ff892e4aa1aae0a0744c39ba76c05c2540ff8c689d768357d9ec293b8b9d4368fd96d735398c5d654c11e1153ba4'], ['e1dbf6843e731dd3b2122fff8045f732407e795f', 'e010790e13b938c882bf642a9666c18d6f4e2bedce30787a73ca10694cdf8194f51df71bf698d5cb65443f6943e000917f003e99b4d2f99dff7b9478f5bbcded0e1d0a80e7703a0496bfe3b96f13ec23'], ['b9d6aae4516ba1a36165eac03f54b06c550d5780', '73a02572f58092ebea5d2e8ab578934e05cb9b502e9bb7e9b83e67d37a2f7f9df16c9c002fceb961694aab0c60b80369a9656466bc3a447d373b2a2a0620081eacd330d18b11fc5199ad3efc8805d91e'], ['e5b6479e2ac1fa782ddad1f1394cb71c0c6116fc', '925977bc2e4789f4eab040cea4f9ed48fa04b09f703ae008f91910a297b30cdf7e3fda555fc0c38515a646bd3f8e7711ba2449140537dd5ced9133351c18b36da09ec29bdf411890792ab408df433700'], ['4345abd256b11382930f02fdc0df3e65115623b4', 'eb356ed0260b01b6c594d13f76349393b5911aefd9efb5f8364737240b64cbb06bafae3fd3d6f7e327e3c8ea7e9424cd1c34ffcfeb1b8b85465ca02b4eef978666c1d8fcb7c37dca769a05e6aa690d35'], ['b94ba2008ceb97173a54d0a6a2d7fb2d60b5560b', '94383dbddc97d1cd212670086ec23b53ae7b863ce885ac66d1e28334ab7ee9ffd478f037eab1305da2a060f4fdd98814f51dbe57e7654ef76cb10bedd7c93567b171837d96149fdf69530676c62fae38'], ['4404c38d757254c21da932d90acd23c93f8f71ef', '472bbd5260db29ef82ce9e3efe94da47c46891b080dad726b9515f3fc37b473eb0760404261ff84297944ad7de89efc343f8e39215e657e64a0e43ccdd72fc077d024968451d04217a194a894656e47a'], ['d9186ef750de0edc19d04f9da49754a4f897621e', '6fa03a03d31da5d740eae597c12aaacf3b53e5e7f9592adf42d82c23472fab16ecc7f47f8b7a1868df3f7d517a34eb89b059ce5d037f448adc64c5eae842572c725be63a1ce361597e890f5e48d75a00'], ['ac15d15d9f17428e9436f7b721365f26acee9d6b', '4c8afd7a48ab8526214455e118f559b649044fd27d7717da0a4492a8ddcad5a0098632a13525ce553e8a4d34afc9ee5875644913d55de2a3cb72c9e5412a4b53abe0763a482a6c4d4079d70308af252f'], ['cf1de82f53d78ec3646be109fe294711b636d03b', 'f930b63c9df3ed9c6b7d7ff4328ee47f8133da448401bedf6490e2c51967c56466de08b0a9670258acfb5fec6330f8eaa4d8820667580fe87af20648a613732c73fad86b791f1aa485553cabba713373'], ['a76f71d544a62fb8c4fc2e50c5279246ac8ce5e3', '28f97e4cbc5fdba4a4941645985356e1c7d216190ada0720dbbe401eac32fb6c2664c395b80e23356530a98e05d674819bc20125e84cbcfa0eabac5f84f2fe7a4b6669224239ef540a99b6fa85aa501e'], ['6438b43851a64990287102993ee0d461a165633e', '0d519bc181a65037247fa9acc82117e0426d244fe6d601a2bbe878b153b1629c8901ffbd719f319c0f8a9c6d094b25cd910a15b2656d612834c79392b2f0b1ae1a355a7db59ae2243ff01d43ee3f5636'], ['d3bdd2213fdf1435637c6e7c6ac7655bb82abcc9', '4fe2d71ea3dbdc3dca467cc9b6c72ca1bcd5a40a9c4ffd02e61f35eab4e49b2b9e2ce5357945803f94f858811837b555a8054249a5a2e69d7922745aa468979794ccfe20ee6783a261ddc9016dc8e407'], ['707fed935a5755c8fb5d76409fa545dcc230bbd9', 'bf6cb543d27a23b79346d0010364898415792be2352e3d9fdb58d01a057be77a6cb3ce78e52d42b150a248227fde1722c0b592f797c55ace2f3f92bca6c2ddc6e525c93f944c7fb25aa1eadd8b992bdc'], ['84bb2d3288bc89ccf9d7ea3d4192af5ab853d4bf', 'ba7f9e95f02b4d8e2d115b4fbe8e800f44080de9e364f5fdbd75a4197f541fc757fa295d3862172670f78096f797b0e8ec3531fc1b7b4506351307956744178a1ec357d457cfa47b5c3616d99fe0b92b'], ['c82abd19b6d45d0b63cdee79712cf0b3bd38f677', 'd96a258ae6bf5c28c4b84bb2f3db5cbe4c5d8b004f8325048f22643b16744de4ca7eb063f2fe07511ed64fcbb7c26f1d9a1bfbf10a72d9d2bdde3ae52c64dc42acadb14f69c9d711a35a195fdfb1dfed'], ['8b8c1801b347aaab00e691f04fa64ed9ccdda653', 'f94f9ebea624b66671b9856afd05e58d87ed8a5124a80e4ad70d53c90d625c6ab2a35a0a4c377bea63f77e364ea3243cd525a39ba4fd9b0cc713f05e0984f479d0a1341eff9c2d6d48852a73d2c0937a'], ['55a36f57bc100971b39ce39478f599692b3f4780', '51c493a7fb2468863926f3c6ae2afd0c7c1a1ecde5780b974ade1214b7320181ee274b9bed203ed7ed80ce64d3872eb07b003c12d54c7ad3bfe57c35b6675b19b58cd460b3e6fd2df0377922c7f5d195'], ['042c3ec5a1e9d737bba74ac72f6485a30b8a15de', '611d15d0998ab039fbe83e40053423cd4b3c31dd6478da927fb5000a0c93573f9980782bbea69bc8f78a110374de58164fb64009f5571db4c636e10acf5f20835dfeb304b9d5c93e0b74b186e7d2cc2a'], ['249c063041f7b2551fe314e6980e6810cce4cb6e', '819b9bf5ca02661b2a1f5e18491bd64b2c3993c4fc8ba2bd41649c36bcd56e2fac87b3841aae6fc5dd448b7b10363c68aff642ded694b5894a3cbd7a92854498d1db73d50685d1b612af9ec0c472baa9'], ['3b29764d0217ea29fece76465febc8a1f6bc223a', '0fba1c353dc6e6e89ef4995052af151eeec0e1bf4e97986979a39831fe1d7f038e5d752abc414e6e9fe0e39a62cffa22580689b7b03f20a5fb1065193ab77fe1a4a56d4f200185f7601215df99de4c79'], ['1589bf490ff2dc0abc43d1036655357ba2c62282', '6d0b690931eae563aa222862db91504982360032c8cfb20610555a0b5d1a538f0426a38130be975fd53e1bacee7a35eeb12d6c9b2687c4d6eea442768544c7ddef4ab491465d835049e2b2615ca977b1'], ['5c2b101e58042b6dc3d1ccd94b97638fc2a22767', '82e4a8a32ad18972b554545f550893618d1fcaeedcf38343998fae6038b101ab9756983b33332c91e0bd85012b6c6b53923f8ca89783ee669f1226da9593ab46403e89c96b95734e2d6621753ced0e2d'], ['8f48920a33f5473a10e9eacb6bf22a1c8b93f4c3', 'd0f152c11a41955827a456139dd0b33216cb179b47f06ca75aff50f56a6278341cd8ab92f7a7de988928e8cb4daf5ba423b39957590c33387853612f0bbc5575e91f62542cf5fe6f5c9da5763294f9de'], ['4b937726382391321688b3c0b756c558eb00d67e', '2a57721a25b5a7833fdca21ef2b5e6c4b625a25de2d00fb85004492605df4a12de41f4185577e58674bcb0428765b7dd698e5e0761194f22782f67c2457569c09ae48b437079632cd847c33a80e68a6d'], ['dcb75155fe55df54b76cb9708bf8c86f4c7a6289', '5bd30c0dcb2c1154a56477d14fb2c2ce88dd6160678da0697bfe7fc43245055ab262b5e750293a09de247a75e0de8aacc97d7d7555cdbe0c389dd9b4ba37a45495a7826b0be78e58d2feb8ec8a23ae8a'], ['29180e9f8cd80e054582c7e54e02af31805eddfd', '0d6fc7d518d85a7bec06b191ad920339cebbd7f2151ed7d453290a39e2753283f5f354ba7f0299ca57f0c795ed50342b2d6d73e7264da401aadda18f0ab462ec2d058e78b5687ee14285737d409fdd2e'], ['58989913a994d2b36c672655d57a64c86ef7993c', '90491f9eece211fc50da1b9c74741a59585795226e29da37ef77bd045aef97840625b4b32a66816f4863780d5d7555d9090288250036107615cc4db9a471da70c21ece34d3174aa57ee45f244a82c283'], ['6edd4a1462e2024f420c739526a0e3f4837144c3', 'e53797068a503b3d5eeff6ed23f5e9a052ee4ee50312080ddf77959164fe3c6cff1a8157abdd840cd54b47ead5f2028a90eb349754910393fe24fb11c3e33204254faadd210f67a0b80840eb75b0b443'], ['3e2265d907b1358a8b1faabdcce88c62c07c2ff5', '748d8ccc7ceae036665952acd77e5aeac2cbc1e5ab9734d9a70a4f3cc30e67e3138e98e54770cb8e9ddd38c2c3a9e11e5acbdf436d4d9b7ada3c62b289599769a11440197a7a963c790b24618817c702'], ['6689f7f226b1f64d7cc4dee575f7c5f15260583a', '0161a325bee56a2ea4757c0979300596f9b96e9af7e005d3189d31939cc54a40640e236774bac9cf2279b72764d88a1b1531d829658cb457fee7c74e2ed237bf85a55626180e6cdb586f5e946a1e9a43'], ['6a123797232e91804b511560cd30fed003b23b8a', '990d97e7d9d32b9273992c30b3394ddee2e87f0e9b34863baa08484b6b368602cc338234ac934ffd50c1f8fcb78c18836bb965a995c178f20765fdcd09d356ece9c30cfccd960b6a86cef4c523fc9fe6'], ['5e992c3b55db669ba5019c7d15755d44115c9165', '4c69280f2a8338943e90fdad3f56a356f33bce5491a3ff68ee9fd0a1a1b115d89d6e723083981afdd4480ada2f86c222ce54d9ca2ece0db4ad3f093553e85be309006ccbc1bccb63862a2277a8360715'], ['e2c10072f61532bc287326772c7cc356b3b7167c', '55a7fb7f784f7d65d59143414fb5cd55b0f56122b956bdb30dbda7ee8f327b588f4e01beaa3902a62c9ba2c90e16b48cf418a9fdb7cef9523889741c91450ec607c00b9b39c50ff062aa8b3927ccfbb4'], ['98d0d351246ca18b5a3322edb5a83ad14a40305b', '5d2940df4451b5ccd30fed6005a620c439ec2f0f8cf7816ff28e803054b1ea6b9507b184d00e5d2f3f5a7e73a5606edae0eefc955f3b4e1e8127b128879f6871d5a717b382302d2645954b9574d23ed2'], ['c212abc676ed5c80fc17bca92a3b9734e6bce9d3', 'e76317a77c69f374eb22cc1d36618c800eab7c9dad72723a3fbb37bed8cf04ca365644d683b8d4ed581dc41ae8d975f2a87bd97e73ed5b6c153cf19864cbd6ddc4d1912aaea1cc015e6c0573a4167fad'], ['bd8cce1b538907201dc070d16416c4641545b7ef', '7b443c01bb0ba008e44b63caf8e580dbc44c0a812d9a2e2be411e281a476b15cb4de6203873409e1a5951cd0e250a5dba5bc031e6bb43773d4fe2a9489902dbfa74f386a7a79850ff569b16e72a889dc'], ['4eb6d2d88c05406a83cf7dd4b30d6613d877fe21', '4e7754804e3a36eafefa0bd8f732a8cc3c947768b8d0a78835221929b815985edb68574aa07b82991e04e2eb41e1b9229b86fc3cb1b3f30e53a1e441d43077dcbf6ca7c4951e00c4a578d7ffe3bb507a'], ['29e72b081931d797ac926fce717c0c28a720f2dd', '46df60c16a9ce3600f3e25feb4ef72d643525db1f1dd47536204bc871fa5ed53ce5ff26b2d2301c6f32ec412f6b6acbb74de6214f4ec9371313ad505f64f87474f743acfb9e516852ed0cafbf71f31c7'], ['451392ebe8c67780093c6ed0f64acf698807e3e3', '433d1d5c69cec372369f09edb8f4f97eb5cfe19b978113527241e74f7a696fd647332b821035d60c02d229d6fb25e16e467fbff6f4a519dd2c3c3afe233353ca771161c60a40491f94a9660a69f659a9'], ['e349350daf45f8d8182bdbf53e70afb267590e7b', 'fc04977344022978927aeaf0db21338da0d168d01cbe215334f40d460fc7c808e44d0870a3f90542ad49cfcee04399e487b8db34409ce4173d618ff280f136d708e911ad21b7ee502b27d9379560ba27'], ['7798405da93666ed72167ddce0b33fd0436be220', '593a1e4831035b59e0bde7eda654de2e954fb0c7cc95caa533c283f127de64b125ecaea691b5e93a6ba8290fa57f00dc91fdc68ebef7425ef729b907303a385102988f95755843d28f48353d1a0adc63'], ['83e45d1665bb75233f1a4e59d7580a8ea5a21ed2', 'c65fb7e4a2ebe243e01e5ad159b6c6c1caa01da3efc31aeb9962a2b3ac72a5b7b9f45f9f7cd596e5ebe59b9d8128b41bfb6d6a13d36f27d320b81b31920676d00ffbfc729dfcd910dfe4611f5252eb0c'], ['54d18f4f667a19d86e3f6cf578d81bb46992f3ec', 'f55f54f22e70e2ffca3d211185e6ac24333be8546daaff6a51542540ebd217f8df21b55bff6e27325ac437cd3a6a26640098d9bdd8311aae3ba73121eb61743d29d79a196355eb6f3e0229dba7c94eca'], ['5b820d300ee30e62d46093df95b537b24a5d6c55', '7ae8a634937c7c7b9285d629c9ebdd729a3cc1caedd8f10dbd13e78bf731fd4aa76433bf2f3161b4a76530e09bd2d0a10b123647d1e2e5635f71f780e83f9dd624a218b66f149b1f5a9ae1e8b9e549b2'], ['04b5da285b8d807264cda3a012539eaf37fb1cce', '1d005d5965820a201aeb189dce35b439d3359827ab6c388ebcc37667f3f527ca15cce2e44c6c4314b1424061bafdb20e16fa8665f62895477a68ea0a28aa8e8d2be78bd8c2c294b5f462947bd4047aca'], ['29c4a76ac4143fff1ac3b61bca1722ab3c98d889', '2acda6afd750a71303a4f12a908bb2e61430b63a658356d00a59f68893ca6d871b090f71e0cc053c4c7ff5527376dd9e3376bfd5aee8e07cee092e7bb3d0bc6d3d1f3626bf946640d964ea7340b2e189'], ['d617ed6a22e0808bf1e2bdac98762a9075fb0fa8', '36d51599bffd9429efa9d138f4081897686efab29c126cf694037874c18fede3a370120deb5b89adedf8551f2c43238641d1337b78a40181187e55b82f689f6034ed46bf25355716517c3596809792f9'], ['8fa85979fcb2083315d27db93de21bc79d69d655', '7f0203e27acac2e54a2d17ef32bca0954fd606f8d1c887c3a93f9692be4b837d0b6a776c395233b921da5436ba7e9d55d87aaa3f81f3bc5db7099821144f1763cf155b6cbd16e478b9f7dfca223eb3bc']]
        while True:
            start_time=time.time()
            message=''
            with open('mentions.json', 'r') as f1:
                was_mentions=json.load(f1)
            mentions=copy.deepcopy(was_mentions)
            for symbol in was_mentions:
                mentions_count = 0
                info=cookies[(f//50)%89]
                try:
                    mentionsrequest=requests.get('https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=('+urllib.parse.quote(was_mentions[symbol]['Magic Eden']['twitter'],safe='')+')%20-filter%3Areplies&tweet_search_mode=live&count=100&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo',
                                                                    headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA','x-csrf-token': info[1]},
                                                                    cookies={' auth_token': info[0], ' ct0': info[1]},
                                                                    timeout=5).json()
                except Exception as e:
                    logger.info(f'1 {e}')
                f+=1
                mentions_count+=len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400, mentionsrequest['globalObjects']['tweets'])))
                cursor=mentionsrequest['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
                while len(mentionsrequest['globalObjects']['tweets'])==len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400, mentionsrequest['globalObjects']['tweets']))) and mentionsrequest['globalObjects']['tweets']:
                    try:
                        info=cookies[(f//50)%89]
                        mentionsrequest=requests.get('https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=('+urllib.parse.quote(was_mentions[symbol]['Magic Eden']['twitter'],safe='')+')%20-filter%3Areplies&tweet_search_mode=live&count=100&query_source=recent_search_click&cursor='+urllib.parse.quote(cursor,safe='')+'&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo',
                                                            headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA','x-csrf-token': info[1]},
                                                            cookies={' auth_token': info[0], ' ct0': info[1]},
                                                            timeout=5).json()
                        mentions_count+=len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsrequest['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400, mentionsrequest['globalObjects']['tweets'])))
                        cursor=mentionsrequest['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']
                        f+=1
                    except Exception as e:
                        logger.info(f'2 {e}')
                mentions[symbol]['mentions']=mentions_count
                try:
                    Magic_Eden_floor=requests.get(f"https://api-mainnet.magiceden.dev/v2/collections/{symbol}/stats",
                                                        timeout=60).json()['floorPrice']/1000000000
                    logger.info(f'{symbol} {Magic_Eden_floor}')
                    mentions[symbol]['Magic Eden']['floor']=Magic_Eden_floor
                    if was_mentions[symbol]['Magic Eden']['floor']!='Just added' and mentions[symbol]['Magic Eden']['floor']>was_mentions[symbol]['Magic Eden']['floor']:
                        try:
                            message+=f"{mentions[symbol]['name']} - упоминания в твиттере {was_mentions[symbol]['mentions']}-->{mentions[symbol]['mentions']}, floor {was_mentions[symbol]['Magic Eden']['floor']}-->{mentions[symbol]['Magic Eden']['floor']}\n"
                        except Exception as e:
                            logger.info(f'4 {e}')
                except Exception as e:
                    logger.info(f'3 {symbol} {e}')
            while message:
                send=message[:message[:4096].rfind('\n')+1]
                message=message[message[:4096].rfind('\n')+1:]
                for user in config.rassilka:
                    bot.send_message(user, send)
                    time.sleep(1)
            with open('mentions.json', 'w') as f1:
                json.dump(mentions,f1)
            del mentions, was_mentions, message
            logger.info(f'Выполнение скрипта завершено {time.strftime("%m-%d-%Y %H:%M:%S",time.gmtime(time.time()))}')
            logger.info(f'Следующий запуск:{time.strftime("%m-%d-%Y %H:%M:%S",time.gmtime(start_time+86400))}')
            time.sleep(86400-(time.time()-start_time))
    except:
        bot.send_message(config.myid, traceback.format_exc())

start()
