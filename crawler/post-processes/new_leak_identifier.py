import base64
import base58
import zlib
import json
import html
import codecs
import brotli
import multiprocessing
from urllib.parse import quote_plus
from lzstring import LZString
from urllib.parse import urlparse
from urllib.parse import parse_qsl
import pandas as pd
import json
from urllib.parse import urlparse, unquote_plus
import csv
import requests
import urllib
import hashlib
import gzip
import shutil
import mmh3
import mmh as mmhash
import base64
import base58
import zlib
import json
import re
from urllib.parse import quote_plus, unquote_plus
import codecs

from lzstring import LZString
import html
import brotli
import lzma

 


PROCESS_RANGE = [0,400]
DOWNLOAD_FOLDER="jsons"
sensitiveWords = {
  "tel": '4922122200',
  "password": 'SaltySeedsTea9!',
  "form_text": 'hi_my_honey_text',
  "form_text2": 'hi_my_honey_field',
  "url_1": 'curious-cat.com',
  "url_2": 'https://curious-cat.com',
  "form_text3": 'my_funny_honey'
};

MY_SENSITIVE_ENCODINGS = set(["hi_my_hone","34393232313232323030", "GQ4TEMRRGIZDEMBQ", "3wAzuvCkRADzGP", "NDkyMjEyMjIwMA==", "4922122200", "33b134323234323232300000", "789c33b1343232343232323000000b0f01f9", "1f8b080000000000001333b134323234323232300000a3e481680a000000", "00110100001110010011001000110010001100010011001000110010001100100011000000110000", "4922122200", "4922122200", "M7E0MjI0MjIyMAAA", "M7E0MjI0MjIyMAAA", "H4sIAAAAAAAAEzOxNDIyNDIyMjAAAKPkgWgKAAAA", "iwSANDkyMjEyMjIwMAM=", "33b134323234323232300000", "1f8b080000000000001333b134323234323232300000a3e481680a000000", "eJwzsTQyMjQyMjIwAAALDwH5", "4KyE7oGM5oKM4ZiA7K2A", "4KyE7oGM5oKM4ZiA7K2A", "CwTgTGCMFgDLQ", "84d3a0756276940932da44e047086405", "7391027a4dcdd6dfa459dfe85e9cd208f7e70ca7", "e2ddeff7f6379160d21bf08d333a18c7b0a290c974f6451903bfc7d301b7df04", "d8f3d7fe7d03fdacc24d4dfca1bba976cf88450b325d25f93c10ba0f", "208aa443dc30af0140762b17e1f268b628fbc7a18515e68104e22eefe9a9a0e5b8e7e07a6a6b073991e66e7bc49c978d", "e1bf1080654ed05dd2a9c0ad2a2b61113febe705d0981fe82a6d3ff0b4c6fbfde33e8a3d5ec73341f233578d3e75a4a4394a6b3290628b9e684e0719b76f323d", "009700fd326c4896ad286fa000671376eacb78ddddc01c58a4381671", "ffbc43328e658b91b896e1a3dc5218c9549357643504cbe1ebcbe7ea0e865247", "69e26e31d0e4489c1717f7cc215ff3824dd359f2dc9b1cf445962a704cf5c511c878ade2887db1d39bbf5f8094b42f4e", "af33a8963c06306fab91e1466c8eb3da039b7149d351db1db55da38dd4f132c26597161fd0bddf002c430642357c31d92e1981f9775cf8f7acde08c1abe22e28", "2022247329", "-2687720209116599037", "3451519139391771119", "63669290229870245713155212006181530883", "1753343139", "185532921","53616C747953656564735465613921", "KNQWY5DZKNSWKZDTKRSWCOJB", "3LJJbd4hWsNsevDznEiiU", "U2FsdHlTZWVkc1RlYTkh", "SaltySeedsTea9%21", "0b4ecc29a90c4e4d4d290e494db4540400", "789c0b4ecc29a90c4e4d4d290e494db45404002ea80576", "1f8b08000000000000130b4ecc29a90c4e4d4d290e494db454040084448f8b0f000000", "010100110110000101101100011101000111100101010011011001010110010101100100011100110101010001100101011000010011100100100001", "SaltySeedsTea9!", "FnyglFrrqfGrn9!", "C07MKakMTk1NKQ5JTbRUBAA=", "C07MKakMTk1NKQ5JTbRUBAA=", "H4sIAAAAAAAAEwtOzCmpDE5NTSkOSU20VAQAhESPiw8AAAA=", "CweAU2FsdHlTZWVkc1RlYTkhAw==", "0b4ecc29a90c4e4d4d290e494db4540400", "1f8b08000000000000130b4ecc29a90c4e4d4d290e494db454040084448f8b0f000000", "eJwLTswpqQxOTU0pDklNtFQEAC6oBXY=", "44qE44C2y6Dpu4DqmrDhjIPjoIXlmKDinIHgooA=", "44qE44C2y6Dpu4DqmrDhjIPjoIXlmKDinIHgooA=", "MoQwNgLgnsCmsBMDOAVWICcBCIA", "4948c713c8f51fcdf341fe5dc5f7f651", "486566dce40fe64622d123079598b9a0bef88551", "2f50045ec0f7fd7ef014aff67338010772fa21226c0b1ca4bb8a596b85a2110f", "2f842ab50309d0bc9db92b5921e71423cc438172313b9e3739669e06", "cb972f03b4d1e1032aecbc095904fd3ce72e0082498eec3fa92b5fa928ca14be586f7838b71c6c7ecde2aedaa2cfe3dc", "d1767a28de17b8862d8d0aebe238048082fa4d43292c941d9e45fee739beea1910d9e528174b0b4597ff9b3b9d0f59eaae00646bb25e74436836b47885bec58c", "12eb75e22875ddf3f4f9df97b55fcdc694a3602ce38b48c03bd709f0", "254b968eda5a4c4ec77b44c5f0c18486b7dcae428586446cc7e32bc4b44efd58", "7f2ea3fbaa3a4655eb902c84e430c2328e98655bb2eba58235067736d62137d923df8578d7dff74439ff42afd8d44ff3", "57ddbf73386b32c4a923a3268ec4837db4e52f84a3eca0b4e2aa6ea1dd87015fe873aa048cb84bf3f3c6790cd1f5dcfadbf67148bbe05f2664f5f6c71702dbdf", "-287875941", "2630329490964472104", "5021836792884838330", "92636538098284972449800741919914713384", "2341422212", "782763382","68695F6D795F686F6E65795F74657874", "NBUV63LZL5UG63TFPFPXIZLYOQ======", "DtohHfG9wm5HUTLmENZzeX", "aGlfbXlfaG9uZXlfdGV4dA==", "hi_my_honey_text", "cbc88ccfad8ccfc8cf4bad8c2f49ad280100", "789ccbc88ccfad8ccfc8cf4bad8c2f49ad280100387106bd", "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c2f49ad2801002ffbe42910000000", "01101000011010010101111101101101011110010101111101101000011011110110111001100101011110010101111101110100011001010111100001110100", "hi_my_honey_text", "uv_zl_ubarl_grkg", "y8iMz62Mz8jPS62ML0mtKAEA", "y8iMz62Mz8jPS62ML0mtKAEA", "H4sIAAAAAAAAE8vIjM+tjM/Iz0utjC9JrSgBAC/75CkQAAAA", "iweAaGlfbXlfaG9uZXlfdGV4dAM=", "cbc88ccfad8ccfc8cf4bad8c2f49ad280100", "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c2f49ad2801002ffbe42910000000", "eJzLyIzPrYzPyM9LrYwvSa0oAQA4cQa9", "1oTrg7rgraDpuazgvaDjrILpo4DiuYjequiAgA==", "1oTrg7rgraDpuazgvaDjrILpo4DiuYjequiAgA==", "BYSw+gtgnmwPYDsCmMAuSAeqg", "43e75bec2b6f2c204cb19a21baf28e34", "eea0bb214e955ddb5eef9c486af767e8fbc5cb39", "1ca570fac198727f82d0010004584b693c6e79b65c923acef84bf4169912ea33", "f6823a0e876191719d95ab3023ee076757ad447377d93b47abf36b90", "44ae82b98381ea880d1135c8ffdd52da3764fe1f1bfb693767ed25c4f6fbab8f04f675e43e5adcaa9b2bcdd07ffcda61", "013c9434fcc85dc02d8d50a38fc2f6495173e053b6d57b8071bd35115ff79ef8a03132d77e7e47ef0fc1e7e9873e3ae27c6b64972362751ef01b3443ad7481b3", "80ad41185430a92c32308e71f8d07ed84c6285a05492946e7bc3168d", "047ba5082a889660c46380e777a8ba2ee4e0dd4bbca69a270e67585454125b46", "f55210fbf2e577b3bc36bc961b960fa3963a7be7878309c847f46f0d7cc4d7b968fe0cf18ecc12b54d4fb7680c56c66a", "2c752ade168750df0fb478e5f8eb9fb821af98d367aee0f916402622a7bc343df8840de8a54a5d505ee96d516451ca6949ad37f0a18ad2b9c93057254e3ee0ef", "1753757807", "-2047910037623045259", "3847981994889785074", "70982739059974200961265151179235885941", "702872367", "946931389", "68695F6D795F686F6E65795F6669656C64", "NBUV63LZL5UG63TFPFPWM2LFNRSA====", "yuf6pXstUhXuiBGECSh1Nzf", "aGlfbXlfaG9uZXlfZmllbGQ=", "hi_my_honey_field", "cbc88ccfad8ccfc8cf4bad8c4fcb4ccd490100", "789ccbc88ccfad8ccfc8cf4bad8c4fcb4ccd4901003f1306fc", "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c4fcb4ccd4901004e4036f511000000", "0110100001101001010111110110110101111001010111110110100001101111011011100110010101111001010111110110011001101001011001010110110001100100", "hi_my_honey_field", "uv_zl_ubarl_svryq", "y8iMz62Mz8jPS62MT8tMzUkBAA==", "y8iMz62Mz8jPS62MT8tMzUkBAA==", "H4sIAAAAAAAAE8vIjM+tjM/Iz0utjE/LTM1JAQBOQDb1EQAAAA==", "CwiAaGlfbXlfaG9uZXlfZmllbGQD", "cbc88ccfad8ccfc8cf4bad8c4fcb4ccd490100", "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c4fcb4ccd4901004e4036f511000000", "eJzLyIzPrYzPyM9LrYxPy0zNSQEAPxMG/A==", "1oTrg7rgraDpuazgvaDjrILpo4DmmKLkgazJpAA=", "1oTrg7rgraDpuazgvaDjrILpo4DmmKLkgazJpAA=", "BYSw+gtgnmwPYDsCmMBmIkBsAmQ", "f505c12230d40a5dd2538d83eedd7da7", "5291e16b1c4f5afef57fb6987b0c838295871e02", "1643c39ff8767f67ee17e7eaf7cb19ce976af8a0b9d3ecc4218111217e372f7d", "b78094ae62a41967e4aa69fd21bee354119d2c56ab68eaffdf197c1c", "3889e1e25d2983e3633edbed592734719c1c6430ec3203aceac3a487129135d20bb2ae1dcd2be66b1fbec52a1c633350", "8b180d4b7d90628533162567bbe3418b2f5520ee7a9de275dd3a0138cf14a7e1893bc8b525bf03772c7328d73e6972686b056b21f2bb03ca2f45c5096b2c9f83", "3a0c7071c21fe32fdb512689ef2e4b16b6ee7f04db7a3df039e49d4b", "de96f137b568833a6f68a4d358ec56bf28e3b1d1d42916a1a0f8afe690c54afe", "86126692cbbf6c0341274afc4c5d98afeca05a7330ef8748d491e87a2df4ae39f01128c6f349f9dccc62e1cd91bd50a9", "23f5e7432d6def6b1517a051f35332f199ea95fae1456242909ca845e977dee52e55110f12ee1ed16cbd139ac0332a7e3e1d0cb60d008e523598e76fa4440cc7", "1248393586", "-6414144220524007930", "-3909599843592213748", "268162979175578004603604889171042938374", "4113973326", "1058211580","637572696F75732D6361742E636F6D", "MN2XE2LPOVZS2Y3BOQXGG33N", "3nPVd4R2N6xz4UUk2Zzhi", "Y3VyaW91cy1jYXQuY29t", "curious-cat.com", "4b2e2dcacc2f2dd64d4e2cd14bcecf0500", "789c4b2e2dcacc2f2dd64d4e2cd14bcecf0500302d05dd", "1f8b08000000000000134b2e2dcacc2f2dd64d4e2cd14bcecf0500c7c1a0530f000000", "011000110111010101110010011010010110111101110101011100110010110101100011011000010111010000101110011000110110111101101101", "curious-cat.com", "phevbhf-png.pbz", "Sy4tyswvLdZNTizRS87PBQA=", "Sy4tyswvLdZNTizRS87PBQA=", "H4sIAAAAAAAAE0suLcrMLy3WTU4s0UvOzwUAx8GgUw8AAAA=", "CweAY3VyaW91cy1jYXQuY29tAw==", "4b2e2dcacc2f2dd64d4e2cd14bcecf0500", "1f8b08000000000000134b2e2dcacc2f2dd64d4e2cd14bcecf0500c7c1a0530f000000", "eJxLLi3KzC8t1k1OLNFLzs8FADAtBd0=", "44aF54GO4KWg75ig7LiL5LCC4aCF7IG07IqB5rKA", "44aF54GO4KWg75ig7LiL5LCC4aCF7IG07IqB5rKA", "MYVwTglg9iDOC0wCGAXAdMKBbIA", "caf5110f98f91040e84a02862066fa65", "b7027c2cda316afe9530e01130788e901fcb7913", "2d216e6c59d921ffeba58dfff2b8581666172fd57bf6ee6e44ad224cb4b45a78", "897f1d1072385b8da1f8f3ca466d346be023f8eb335192fce69cea70", "a50db105ebf563ca079ecfd786f943a0e0e392b762a387ad129bc3fff3b468cc15e2ededf353c681456551eaa3bd6137", "9a8b60802fe42fb6aae650c391181b1e54c3a0f8efd1a180b4d698f0a6cdeceeb694c0f740cffbf49c75f0634c18283fff3c3380e5710774616b39a68a8c9bbb", "ef2d53be51971fb181b05ac122cd1f67407624fe9b22fd3d062d21b4", "0915e1bf120f2dc9d303b2a2e7a19938bfa1a78921238eb1776d2fbacd25cb5a", "2def97b3ff239ce0096eaa28aa320fa717f2381c7000c46cec7e0fcae6d3f475ea712b5a6b8b5915665b0d82231a5b6c", "cf9b6c7ac1c7f44f3eda22592edd8094e97e5d04b00f830365d024be8ad3f15c559194d8ec5bad598e567b562698ec4fe5a9a363363450b4ed2419564c1be4b8", "-679406168", "2755373884543779069", "-3309345380778307472", "279235719630208140617208984455809515773", "1403044295", "808256989","68747470733A2F2F637572696F75732D6361742E636F6D", "NB2HI4DTHIXS6Y3VOJUW65LTFVRWC5BOMNXW2===", "3A8evQZovd7B4jbwRyktga3ZR6388nYC", "aHR0cHM6Ly9jdXJpb3VzLWNhdC5jb20=", "https%3A%2F%2Fcurious-cat.com", "cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500", "789ccb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500687508a8", "1f8b0800000000000013cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500b9e6387817000000", "0110100001110100011101000111000001110011001110100010111100101111011000110111010101110010011010010110111101110101011100110010110101100011011000010111010000101110011000110110111101101101", "https://curious-cat.com", "uggcf://phevbhf-png.pbz", "yygpKSi20tdPLi3KzC8t1k1OLNFLzs8FAA==", "yygpKSi20tdPLi3KzC8t1k1OLNFLzs8FAA==", "H4sIAAAAAAAAE8soKSkottLXTy4tyswvLdZNTizRS87PBQC55jh4FwAAAA==", "GxYA+MVTFpMaTJJsfhWMQGWKSyTptDo7iE8=", "cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500", "1f8b0800000000000013cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500b9e6387817000000", "eJzLKCkpKLbS108uLcrMLy3WTU4s0UvOzwUAaHUIqA==", "1oHnhIHshpzgroHupaDsmIXngJPohKzgvaTsoJbohITjhIDjqITjgJbsoIA=", "1oHnhIHshpzgroHupaDsmIXngJPohKzgvaTsoJbohITjhIDjqITjgJbsoIA=", "BYFxAcGcC4HpYMYFcBOBLA9kyBaBBDEAOgQwFsg", "c1a8de3f62604990390ff0555a524865", "41982bd1605b895577c73fe915e0d341c880fb60", "c9b19caac3fa71da9addc8270a4769744ea11f2a6a5edc27ebc1c532951cc291", "ed944b6e4b7a5d8d3124a20099f6126f46d398f793b9623229c108e1", "945e4b8f11d001863cc3ad23d239d8405484b673ba7e5f3039c7d55b32e20a72634b478f9a69f9c30beac7becf86ad8e", "938ca936fd2bcdff508bbea2c5665c2d4f618129c41a9fa88ad40917b9402150ee4836d26b1946d357476e0d2c7e1cad32b792faa45740474e0e7cafd94d8ffb", "6c901274c1162a4c9bd9a8580e06b6c2d3e4724ee62bfe89954b81cc", "c1d03e01aaa3442521f7d9d45fbbc02e38ce550103ac44303f511ffee6d3dc88", "47f9f776c15a87028a6b82e22acfd25c847c0a6d71ebf25749e0244c9957412799cb1eb83055d2c50ab94e2a86b1485e", "2c05c2c4dd2d3b0b967cd25fc742ac7749c058d79f913340ed51e3950f8abca92ab770ab3d3fd0af8da10b910fc5bfa94e4173891279bd7072ee53aa49d54c00", "1166678749", "2131491993515325067", "-5174759824637364236", "244824896792938886174747607789649131147", "2016995001", "1752500392","6D795F66756E6E795F686F6E6579", "NV4V6ZTVNZXHSX3IN5XGK6I=", "hFHucvJjLBAotAF5wEG", "bXlfZnVubnlfaG9uZXk=", "my_funny_honey", "cbad8c4f2bcdcbab8ccfc8cf4bad0400", "789ccbad8c4f2bcdcbab8ccfc8cf4bad04002cb905f8", "1f8b0800000000000013cbad8c4f2bcdcbab8ccfc8cf4bad0400ef8be65d0e000000", "0110110101111001010111110110011001110101011011100110111001111001010111110110100001101111011011100110010101111001", "my_funny_honey", "zl_shaal_ubarl", "y62MTyvNy6uMz8jPS60EAA==", "y62MTyvNy6uMz8jPS60EAA==", "H4sIAAAAAAAAE8utjE8rzcurjM/Iz0utBADvi+ZdDgAAAA==", "iwaAbXlfZnVubnlfaG9uZXkD", "cbad8c4f2bcdcbab8ccfc8cf4bad0400", "1f8b0800000000000013cbad8c4f2bcdcbab8ccfc8cf4bad0400ef8be65d0e000000", "eJzLrYxPK83Lq4zPyM9LrQQALLkF+A==", "4raE74O62aDquIfmj6DgrIPto4DqmKIA", "4raE74O62aDquIfmj6DgrIPto4DqmKIA", "LYTw+gZgrgdj4AsD2MCmIg", "30247d2340349e67ba677a358aeb51c2", "f85059d378904b17af1af3dffd1c006eb3a0d5a9", "dbd3135a7d724f50502c59fe740c4129ccf538b3b0a936a9aa0323e867f86cbb", "a34d74db44abd71b5f546ab366494f2cc808c2121f898d436e02c457", "99b4ff2d3c53f20a5a1815bcabeed1cfc66659fb0e9a960981ff981e4a7b808a496ec646ff1d9e7893dc7b5ed845ff11", "1691253552841a376371107fdf3628b9432dac01a05f3cc041875adeedddba886fd0765d9dac2e565452d82d5fb1d9602d4d971f7b74da71ae7eef0610f91270", "31be1bb1e2a65f888b19aafe249c9131d62508aacd81981593218561", "dbaa7e4a281ef017b87ab8afab5bd2b4f741e94a1106d2a6a97fd75d8550ac6e", "e34c0002d6a3da03d275ee17afd512629a95bef472bbe16272212d490c1b90ed037cc8821beea3283c260844f15bbda3", "373297e145c92a81a9de0216cf2cba7acd4626dd0537afead6e1db2c37b634e6f4c19ad59382959398f992c60207467b80a6339bcb2848a516f7eeff26f70cee", "-1229217392", "-8568163609771675660", "-511827998734884535", "330840806818517112295286193563323428852", "1575390191", "750323192" ])


MY_SENSITIVE_ENCODINGS= {
  "tel": [
    "34393232313232323030",
    "GQ4TEMRRGIZDEMBQ",
    "3wAzuvCkRADzGP",
    "NDkyMjEyMjIwMA==",
    "4922122200",
    "33b134323234323232300000",
    "789c33b1343232343232323000000b0f01f9",
    "1f8b080000000000001333b134323234323232300000a3e481680a000000",
    "00110100001110010011001000110010001100010011001000110010001100100011000000110000",
    "4922122200",
    "4922122200",
    "M7E0MjI0MjIyMAAA",
    "M7E0MjI0MjIyMAAA",
    "H4sIAAAAAAAAEzOxNDIyNDIyMjAAAKPkgWgKAAAA",
    "iwSANDkyMjEyMjIwMAM=",
    "33b134323234323232300000",
    "1f8b080000000000001333b134323234323232300000a3e481680a000000",
    "eJwzsTQyMjQyMjIwAAALDwH5",
    "4KyE7oGM5oKM4ZiA7K2A",
    "4KyE7oGM5oKM4ZiA7K2A",
    "CwTgTGCMFgDLQ",
    "84d3a0756276940932da44e047086405",
    "7391027a4dcdd6dfa459dfe85e9cd208f7e70ca7",
    "e2ddeff7f6379160d21bf08d333a18c7b0a290c974f6451903bfc7d301b7df04",
    "d8f3d7fe7d03fdacc24d4dfca1bba976cf88450b325d25f93c10ba0f",
    "208aa443dc30af0140762b17e1f268b628fbc7a18515e68104e22eefe9a9a0e5b8e7e07a6a6b073991e66e7bc49c978d",
    "e1bf1080654ed05dd2a9c0ad2a2b61113febe705d0981fe82a6d3ff0b4c6fbfde33e8a3d5ec73341f233578d3e75a4a4394a6b3290628b9e684e0719b76f323d",
    "009700fd326c4896ad286fa000671376eacb78ddddc01c58a4381671",
    "ffbc43328e658b91b896e1a3dc5218c9549357643504cbe1ebcbe7ea0e865247",
    "69e26e31d0e4489c1717f7cc215ff3824dd359f2dc9b1cf445962a704cf5c511c878ade2887db1d39bbf5f8094b42f4e",
    "af33a8963c06306fab91e1466c8eb3da039b7149d351db1db55da38dd4f132c26597161fd0bddf002c430642357c31d92e1981f9775cf8f7acde08c1abe22e28",
    "2022247329",
    "-2687720209116599037",
    "3451519139391771119",
    "63669290229870245713155212006181530883",
    "1753343139",
    "185532921"
  ],
  "password": [
    "53616C747953656564735465613921",
    "KNQWY5DZKNSWKZDTKRSWCOJB",
    "3LJJbd4hWsNsevDznEiiU",
    "U2FsdHlTZWVkc1RlYTkh",
    "SaltySeedsTea9%21",
    "0b4ecc29a90c4e4d4d290e494db4540400",
    "789c0b4ecc29a90c4e4d4d290e494db45404002ea80576",
    "1f8b08000000000000130b4ecc29a90c4e4d4d290e494db454040084448f8b0f000000",
    "010100110110000101101100011101000111100101010011011001010110010101100100011100110101010001100101011000010011100100100001",
    "SaltySeedsTea9!",
    "FnyglFrrqfGrn9!",
    "C07MKakMTk1NKQ5JTbRUBAA=",
    "C07MKakMTk1NKQ5JTbRUBAA=",
    "H4sIAAAAAAAAEwtOzCmpDE5NTSkOSU20VAQAhESPiw8AAAA=",
    "CweAU2FsdHlTZWVkc1RlYTkhAw==",
    "0b4ecc29a90c4e4d4d290e494db4540400",
    "1f8b08000000000000130b4ecc29a90c4e4d4d290e494db454040084448f8b0f000000",
    "eJwLTswpqQxOTU0pDklNtFQEAC6oBXY=",
    "44qE44C2y6Dpu4DqmrDhjIPjoIXlmKDinIHgooA=",
    "44qE44C2y6Dpu4DqmrDhjIPjoIXlmKDinIHgooA=",
    "MoQwNgLgnsCmsBMDOAVWICcBCIA",
    "4948c713c8f51fcdf341fe5dc5f7f651",
    "486566dce40fe64622d123079598b9a0bef88551",
    "2f50045ec0f7fd7ef014aff67338010772fa21226c0b1ca4bb8a596b85a2110f",
    "2f842ab50309d0bc9db92b5921e71423cc438172313b9e3739669e06",
    "cb972f03b4d1e1032aecbc095904fd3ce72e0082498eec3fa92b5fa928ca14be586f7838b71c6c7ecde2aedaa2cfe3dc",
    "d1767a28de17b8862d8d0aebe238048082fa4d43292c941d9e45fee739beea1910d9e528174b0b4597ff9b3b9d0f59eaae00646bb25e74436836b47885bec58c",
    "12eb75e22875ddf3f4f9df97b55fcdc694a3602ce38b48c03bd709f0",
    "254b968eda5a4c4ec77b44c5f0c18486b7dcae428586446cc7e32bc4b44efd58",
    "7f2ea3fbaa3a4655eb902c84e430c2328e98655bb2eba58235067736d62137d923df8578d7dff74439ff42afd8d44ff3",
    "57ddbf73386b32c4a923a3268ec4837db4e52f84a3eca0b4e2aa6ea1dd87015fe873aa048cb84bf3f3c6790cd1f5dcfadbf67148bbe05f2664f5f6c71702dbdf",
    "-287875941",
    "2630329490964472104",
    "5021836792884838330",
    "92636538098284972449800741919914713384",
    "2341422212",
    "782763382"
  ],
  "form_text": [
    "68695F6D795F686F6E65795F74657874",
    "NBUV63LZL5UG63TFPFPXIZLYOQ======",
    "DtohHfG9wm5HUTLmENZzeX",
    "aGlfbXlfaG9uZXlfdGV4dA==",
    "hi_my_hone",
    "hi_my_honey_text",
    "cbc88ccfad8ccfc8cf4bad8c2f49ad280100",
    "789ccbc88ccfad8ccfc8cf4bad8c2f49ad280100387106bd",
    "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c2f49ad2801002ffbe42910000000",
    "01101000011010010101111101101101011110010101111101101000011011110110111001100101011110010101111101110100011001010111100001110100",
    "hi_my_honey_text",
    "hi_my_honey_tex"
    "uv_zl_ubarl_grkg",
    "y8iMz62Mz8jPS62ML0mtKAEA",
    "y8iMz62Mz8jPS62ML0mtKAEA",
    "H4sIAAAAAAAAE8vIjM+tjM/Iz0utjC9JrSgBAC/75CkQAAAA",
    "iweAaGlfbXlfaG9uZXlfdGV4dAM=",
    "cbc88ccfad8ccfc8cf4bad8c2f49ad280100",
    "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c2f49ad2801002ffbe42910000000",
    "eJzLyIzPrYzPyM9LrYwvSa0oAQA4cQa9",
    "1oTrg7rgraDpuazgvaDjrILpo4DiuYjequiAgA==",
    "1oTrg7rgraDpuazgvaDjrILpo4DiuYjequiAgA==",
    "BYSw+gtgnmwPYDsCmMAuSAeqg",
    "43e75bec2b6f2c204cb19a21baf28e34",
    "eea0bb214e955ddb5eef9c486af767e8fbc5cb39",
    "1ca570fac198727f82d0010004584b693c6e79b65c923acef84bf4169912ea33",
    "f6823a0e876191719d95ab3023ee076757ad447377d93b47abf36b90",
    "44ae82b98381ea880d1135c8ffdd52da3764fe1f1bfb693767ed25c4f6fbab8f04f675e43e5adcaa9b2bcdd07ffcda61",
    "013c9434fcc85dc02d8d50a38fc2f6495173e053b6d57b8071bd35115ff79ef8a03132d77e7e47ef0fc1e7e9873e3ae27c6b64972362751ef01b3443ad7481b3",
    "80ad41185430a92c32308e71f8d07ed84c6285a05492946e7bc3168d",
    "047ba5082a889660c46380e777a8ba2ee4e0dd4bbca69a270e67585454125b46",
    "f55210fbf2e577b3bc36bc961b960fa3963a7be7878309c847f46f0d7cc4d7b968fe0cf18ecc12b54d4fb7680c56c66a",
    "2c752ade168750df0fb478e5f8eb9fb821af98d367aee0f916402622a7bc343df8840de8a54a5d505ee96d516451ca6949ad37f0a18ad2b9c93057254e3ee0ef",
    "1753757807",
    "-2047910037623045259",
    "3847981994889785074",
    "70982739059974200961265151179235885941",
    "702872367",
    "946931389"
  ],
  "form_text2": [
    "68695F6D795F686F6E65795F6669656C64",
    "NBUV63LZL5UG63TFPFPWM2LFNRSA====",
    "yuf6pXstUhXuiBGECSh1Nzf",
    "aGlfbXlfaG9uZXlfZmllbGQ=",
    "hi_my_honey_field",
    "cbc88ccfad8ccfc8cf4bad8c4fcb4ccd490100",
    "789ccbc88ccfad8ccfc8cf4bad8c4fcb4ccd4901003f1306fc",
    "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c4fcb4ccd4901004e4036f511000000",
    "0110100001101001010111110110110101111001010111110110100001101111011011100110010101111001010111110110011001101001011001010110110001100100",
    "hi_my_honey_field",
    "uv_zl_ubarl_svryq",
    "y8iMz62Mz8jPS62MT8tMzUkBAA==",
    "y8iMz62Mz8jPS62MT8tMzUkBAA==",
    "H4sIAAAAAAAAE8vIjM+tjM/Iz0utjE/LTM1JAQBOQDb1EQAAAA==",
    "CwiAaGlfbXlfaG9uZXlfZmllbGQD",
    "cbc88ccfad8ccfc8cf4bad8c4fcb4ccd490100",
    "1f8b0800000000000013cbc88ccfad8ccfc8cf4bad8c4fcb4ccd4901004e4036f511000000",
    "eJzLyIzPrYzPyM9LrYxPy0zNSQEAPxMG/A==",
    "1oTrg7rgraDpuazgvaDjrILpo4DmmKLkgazJpAA=",
    "1oTrg7rgraDpuazgvaDjrILpo4DmmKLkgazJpAA=",
    "BYSw+gtgnmwPYDsCmMBmIkBsAmQ",
    "f505c12230d40a5dd2538d83eedd7da7",
    "5291e16b1c4f5afef57fb6987b0c838295871e02",
    "1643c39ff8767f67ee17e7eaf7cb19ce976af8a0b9d3ecc4218111217e372f7d",
    "b78094ae62a41967e4aa69fd21bee354119d2c56ab68eaffdf197c1c",
    "3889e1e25d2983e3633edbed592734719c1c6430ec3203aceac3a487129135d20bb2ae1dcd2be66b1fbec52a1c633350",
    "8b180d4b7d90628533162567bbe3418b2f5520ee7a9de275dd3a0138cf14a7e1893bc8b525bf03772c7328d73e6972686b056b21f2bb03ca2f45c5096b2c9f83",
    "3a0c7071c21fe32fdb512689ef2e4b16b6ee7f04db7a3df039e49d4b",
    "de96f137b568833a6f68a4d358ec56bf28e3b1d1d42916a1a0f8afe690c54afe",
    "86126692cbbf6c0341274afc4c5d98afeca05a7330ef8748d491e87a2df4ae39f01128c6f349f9dccc62e1cd91bd50a9",
    "23f5e7432d6def6b1517a051f35332f199ea95fae1456242909ca845e977dee52e55110f12ee1ed16cbd139ac0332a7e3e1d0cb60d008e523598e76fa4440cc7",
    "1248393586",
    "-6414144220524007930",
    "-3909599843592213748",
    "268162979175578004603604889171042938374",
    "4113973326",
    "1058211580"
  ],
  "url_1": [
    "637572696F75732D6361742E636F6D",
    "MN2XE2LPOVZS2Y3BOQXGG33N",
    "3nPVd4R2N6xz4UUk2Zzhi",
    "Y3VyaW91cy1jYXQuY29t",
    "curious-cat.com",
    "4b2e2dcacc2f2dd64d4e2cd14bcecf0500",
    "789c4b2e2dcacc2f2dd64d4e2cd14bcecf0500302d05dd",
    "1f8b08000000000000134b2e2dcacc2f2dd64d4e2cd14bcecf0500c7c1a0530f000000",
    "011000110111010101110010011010010110111101110101011100110010110101100011011000010111010000101110011000110110111101101101",
    "curious-cat.com",
    "phevbhf-png.pbz",
    "Sy4tyswvLdZNTizRS87PBQA=",
    "Sy4tyswvLdZNTizRS87PBQA=",
    "H4sIAAAAAAAAE0suLcrMLy3WTU4s0UvOzwUAx8GgUw8AAAA=",
    "CweAY3VyaW91cy1jYXQuY29tAw==",
    "4b2e2dcacc2f2dd64d4e2cd14bcecf0500",
    "1f8b08000000000000134b2e2dcacc2f2dd64d4e2cd14bcecf0500c7c1a0530f000000",
    "eJxLLi3KzC8t1k1OLNFLzs8FADAtBd0=",
    "44aF54GO4KWg75ig7LiL5LCC4aCF7IG07IqB5rKA",
    "44aF54GO4KWg75ig7LiL5LCC4aCF7IG07IqB5rKA",
    "MYVwTglg9iDOC0wCGAXAdMKBbIA",
    "caf5110f98f91040e84a02862066fa65",
    "b7027c2cda316afe9530e01130788e901fcb7913",
    "2d216e6c59d921ffeba58dfff2b8581666172fd57bf6ee6e44ad224cb4b45a78",
    "897f1d1072385b8da1f8f3ca466d346be023f8eb335192fce69cea70",
    "a50db105ebf563ca079ecfd786f943a0e0e392b762a387ad129bc3fff3b468cc15e2ededf353c681456551eaa3bd6137",
    "9a8b60802fe42fb6aae650c391181b1e54c3a0f8efd1a180b4d698f0a6cdeceeb694c0f740cffbf49c75f0634c18283fff3c3380e5710774616b39a68a8c9bbb",
    "ef2d53be51971fb181b05ac122cd1f67407624fe9b22fd3d062d21b4",
    "0915e1bf120f2dc9d303b2a2e7a19938bfa1a78921238eb1776d2fbacd25cb5a",
    "2def97b3ff239ce0096eaa28aa320fa717f2381c7000c46cec7e0fcae6d3f475ea712b5a6b8b5915665b0d82231a5b6c",
    "cf9b6c7ac1c7f44f3eda22592edd8094e97e5d04b00f830365d024be8ad3f15c559194d8ec5bad598e567b562698ec4fe5a9a363363450b4ed2419564c1be4b8",
    "-679406168",
    "2755373884543779069",
    "-3309345380778307472",
    "279235719630208140617208984455809515773",
    "1403044295",
    "808256989"
  ],
  "url_2": [
    "68747470733A2F2F637572696F75732D6361742E636F6D",
    "NB2HI4DTHIXS6Y3VOJUW65LTFVRWC5BOMNXW2===",
    "3A8evQZovd7B4jbwRyktga3ZR6388nYC",
    "aHR0cHM6Ly9jdXJpb3VzLWNhdC5jb20=",
    "https%3A%2F%2Fcurious-cat.com",
    "cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500",
    "789ccb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500687508a8",
    "1f8b0800000000000013cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500b9e6387817000000",
    "0110100001110100011101000111000001110011001110100010111100101111011000110111010101110010011010010110111101110101011100110010110101100011011000010111010000101110011000110110111101101101",
    "https://curious-cat.com",
    "uggcf://phevbhf-png.pbz",
    "yygpKSi20tdPLi3KzC8t1k1OLNFLzs8FAA==",
    "yygpKSi20tdPLi3KzC8t1k1OLNFLzs8FAA==",
    "H4sIAAAAAAAAE8soKSkottLXTy4tyswvLdZNTizRS87PBQC55jh4FwAAAA==",
    "GxYA+MVTFpMaTJJsfhWMQGWKSyTptDo7iE8=",
    "cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500",
    "1f8b0800000000000013cb28292928b6d2d74f2e2dcacc2f2dd64d4e2cd14bcecf0500b9e6387817000000",
    "eJzLKCkpKLbS108uLcrMLy3WTU4s0UvOzwUAaHUIqA==",
    "1oHnhIHshpzgroHupaDsmIXngJPohKzgvaTsoJbohITjhIDjqITjgJbsoIA=",
    "1oHnhIHshpzgroHupaDsmIXngJPohKzgvaTsoJbohITjhIDjqITjgJbsoIA=",
    "BYFxAcGcC4HpYMYFcBOBLA9kyBaBBDEAOgQwFsg",
    "c1a8de3f62604990390ff0555a524865",
    "41982bd1605b895577c73fe915e0d341c880fb60",
    "c9b19caac3fa71da9addc8270a4769744ea11f2a6a5edc27ebc1c532951cc291",
    "ed944b6e4b7a5d8d3124a20099f6126f46d398f793b9623229c108e1",
    "945e4b8f11d001863cc3ad23d239d8405484b673ba7e5f3039c7d55b32e20a72634b478f9a69f9c30beac7becf86ad8e",
    "938ca936fd2bcdff508bbea2c5665c2d4f618129c41a9fa88ad40917b9402150ee4836d26b1946d357476e0d2c7e1cad32b792faa45740474e0e7cafd94d8ffb",
    "6c901274c1162a4c9bd9a8580e06b6c2d3e4724ee62bfe89954b81cc",
    "c1d03e01aaa3442521f7d9d45fbbc02e38ce550103ac44303f511ffee6d3dc88",
    "47f9f776c15a87028a6b82e22acfd25c847c0a6d71ebf25749e0244c9957412799cb1eb83055d2c50ab94e2a86b1485e",
    "2c05c2c4dd2d3b0b967cd25fc742ac7749c058d79f913340ed51e3950f8abca92ab770ab3d3fd0af8da10b910fc5bfa94e4173891279bd7072ee53aa49d54c00",
    "1166678749",
    "2131491993515325067",
    "-5174759824637364236",
    "244824896792938886174747607789649131147",
    "2016995001",
    "1752500392"
  ],
  "form_text3": [
    "6D795F66756E6E795F686F6E6579",
    "NV4V6ZTVNZXHSX3IN5XGK6I=",
    "hFHucvJjLBAotAF5wEG",
    "bXlfZnVubnlfaG9uZXk=",
    "my_funny_honey",
    "cbad8c4f2bcdcbab8ccfc8cf4bad0400",
    "789ccbad8c4f2bcdcbab8ccfc8cf4bad04002cb905f8",
    "1f8b0800000000000013cbad8c4f2bcdcbab8ccfc8cf4bad0400ef8be65d0e000000",
    "0110110101111001010111110110011001110101011011100110111001111001010111110110100001101111011011100110010101111001",
    "my_funny_honey",
    "zl_shaal_ubarl",
    "y62MTyvNy6uMz8jPS60EAA==",
    "y62MTyvNy6uMz8jPS60EAA==",
    "H4sIAAAAAAAAE8utjE8rzcurjM/Iz0utBADvi+ZdDgAAAA==",
    "iwaAbXlfZnVubnlfaG9uZXkD",
    "cbad8c4f2bcdcbab8ccfc8cf4bad0400",
    "1f8b0800000000000013cbad8c4f2bcdcbab8ccfc8cf4bad0400ef8be65d0e000000",
    "eJzLrYxPK83Lq4zPyM9LrQQALLkF+A==",
    "4raE74O62aDquIfmj6DgrIPto4DqmKIA",
    "4raE74O62aDquIfmj6DgrIPto4DqmKIA",
    "LYTw+gZgrgdj4AsD2MCmIg",
    "30247d2340349e67ba677a358aeb51c2",
    "f85059d378904b17af1af3dffd1c006eb3a0d5a9",
    "dbd3135a7d724f50502c59fe740c4129ccf538b3b0a936a9aa0323e867f86cbb",
    "a34d74db44abd71b5f546ab366494f2cc808c2121f898d436e02c457",
    "99b4ff2d3c53f20a5a1815bcabeed1cfc66659fb0e9a960981ff981e4a7b808a496ec646ff1d9e7893dc7b5ed845ff11",
    "1691253552841a376371107fdf3628b9432dac01a05f3cc041875adeedddba886fd0765d9dac2e565452d82d5fb1d9602d4d971f7b74da71ae7eef0610f91270",
    "31be1bb1e2a65f888b19aafe249c9131d62508aacd81981593218561",
    "dbaa7e4a281ef017b87ab8afab5bd2b4f741e94a1106d2a6a97fd75d8550ac6e",
    "e34c0002d6a3da03d275ee17afd512629a95bef472bbe16272212d490c1b90ed037cc8821beea3283c260844f15bbda3",
    "373297e145c92a81a9de0216cf2cba7acd4626dd0537afead6e1db2c37b634e6f4c19ad59382959398f992c60207467b80a6339bcb2848a516f7eeff26f70cee",
    "-1229217392",
    "-8568163609771675660",
    "-511827998734884535",
    "330840806818517112295286193563323428852",
    "1575390191",
    "750323192"
  ]
}

MIN_LENGTH_OF_FIELD = 10 # Minimum length of field to be considered a token

def find_matches(sensitive_dict, candidates):
    
   # print(f"Finding matches in {len(candidates)} candidates...")
    
  #  print("sensitive_dict: ", sensitive_dict)
  #  print("candidates: ", candidates)
    matches = set()
    candidate_strs = list(map(str, candidates))  # Ensure all are strings
    concatenated = ' '.join(candidate_strs)      # Concatenate once for faster lookup
 
    
    for key, values in sensitive_dict.items():
        unique_values = set(values)  # Deduplicate sensitive values
        for val in unique_values:
            val_str = str(val)
            if val_str in concatenated:
                if isinstance(key, (str, int, float)):
                    matches.add(str(key)) 
                else:
                    print(f"Skipping unhashable key: {key} (type: {type(key)})")
                break  # No need to check more values for this key

    return list(matches)
def compress_with_zlib(compression_type, string, level=6):
    if compression_type == 'deflate':
        compressor = zlib.compressobj(level, zlib.DEFLATED, -zlib.MAX_WBITS)
    elif compression_type == 'zlib':
        compressor = zlib.compressobj(level, zlib.DEFLATED, zlib.MAX_WBITS)
    elif compression_type == 'gzip':
        compressor = zlib.compressobj(level, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    else:
        raise ValueError(f"Unsupported zlib compression format: {compression_type}")
    return compressor.compress(string) + compressor.flush()


def create_variations(input_string):
    x_bytes = input_string.encode('utf-8')
    x_str = input_string
    results = {}

    encodings = {
        'base16': lambda x: base64.b16encode(x),
        'base32': lambda x: base64.b32encode(x),
        'base58': lambda x: base58.b58encode(x),
        'base64': lambda x: base64.b64encode(x),
        'urlencode': lambda x: quote_plus(x_str),
        'deflate': lambda x: compress_with_zlib('deflate', x),
        'zlib': lambda x: compress_with_zlib('zlib', x),
        'gzip': lambda x: compress_with_zlib('gzip', x), 
        'binary': lambda x: ''.join(format(b, '08b') for b in x),
        'entity': lambda x: html.escape(x_str),
        'rot13': lambda x: codecs.encode(x_str, 'rot_13'),
        'deflate_base64': lambda x: base64.b64encode(compress_with_zlib('deflate', x)),
        'deflateraw_base64': lambda x: base64.b64encode(compress_with_zlib('deflate', x)),
        'gzip_base64': lambda x: base64.b64encode(compress_with_zlib('gzip', x)),
        'brotli_base64': lambda x: base64.b64encode(brotli.compress(x)),
        'deflate_hex': lambda x: compress_with_zlib('deflate', x).hex(),
        'gzip_hex': lambda x: compress_with_zlib('gzip', x).hex(),
        'zlib64': lambda x: base64.b64encode(zlib.compress(x)).decode('utf-8')
    }  

    # Optional encodings (wrapped in try-except)
    try:
        lz = LZString()
        encodings['lz64'] = lambda x: base64.b64encode(
            lz.compress(x.decode('utf-8')).encode('utf-8', errors='surrogatepass')
        )
        encodings['lz64de'] = lambda x: base64.b64encode(
            LZString().compress(x.decode('utf-8')).encode('utf-8', errors='surrogatepass')
        ).decode('utf-8', errors='ignore')
        encodings['lz_string'] = lambda x: lz.compressToEncodedURIComponent(x_str)
    except Exception:
        pass

    try:
        import lzw
        encodings['lzw'] = lambda x: json.dumps(lzw.encode(x_str))
    except Exception:
        pass
    
    hashes = dict()
    # hashes['md2'] = lambda x: self._get_md2_hash(x)
    encodings['md5'] = lambda x: hashlib.md5(x).hexdigest()
    encodings['sha1'] = lambda x: hashlib.sha1(x).hexdigest()
    encodings['sha256'] = lambda x: hashlib.sha256(x).hexdigest()
    encodings['sha224'] = lambda x: hashlib.sha224(x).hexdigest()
    encodings['sha384'] = lambda x: hashlib.sha384(x).hexdigest()
    encodings['sha512'] = lambda x: hashlib.sha512(x).hexdigest()
    encodings['sha3_224'] = lambda x: hashlib.sha3_224(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
    encodings['sha3_256'] = lambda x: hashlib.sha3_256(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
    encodings['sha3_384'] = lambda x: hashlib.sha3_384(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
    encodings['sha3_512'] = lambda x: hashlib.sha3_512(x if isinstance(x, bytes) else x.encode('utf-8')).hexdigest()
    encodings['mmh3_32'] = lambda x: str(mmh3.hash(x))
    encodings['mmh3_64_1'] = lambda x: str(mmh3.hash64(x)[0])
    encodings['mmh3_64_2'] = lambda x: str(mmh3.hash64(x)[1])
    encodings['mmh3_128'] = lambda x: str(mmh3.hash128(x))
    # hashes['blake2b'] = lambda x: pyblake2.blake2b(x).hexdigest()
    # hashes['blake2s'] = lambda x: pyblake2.blake2s(x).hexdigest()
    encodings['crc32'] = lambda x: str(zlib.crc32(x) & 0xFFFFFFFF)
    encodings['adler32'] = lambda x: str(zlib.adler32(x))
 
    
    
    # Apply all encodings
    for name, func in encodings.items():
        try:
            result = func(x_bytes)
            if isinstance(result, bytes):
                try:
                    results[name] = result.decode('utf-8')
                except UnicodeDecodeError:
                    results[name] = result.hex()
            else:
                results[name] = result
        except Exception as e:
            results[name] = f'ERROR: {str(e)}'
            
    return results


def _decompress_with_zlib(self, compression_type, string, level=9):
    """Compress in one of the zlib supported formats: zlib, gzip, or deflate.
    For a description see: http://stackoverflow.com/a/22311297/6073564
    """
    if compression_type == 'deflate':
        return zlib.decompress(string, -zlib.MAX_WBITS)
    elif compression_type == 'zlib':
        return zlib.decompress(string, zlib.MAX_WBITS)
    elif compression_type == 'gzip':
        return zlib.decompress(string, zlib.MAX_WBITS | 16)
    else:
        raise ValueError("Unsupported zlib compression format %s." %
                compression_type)


def decode_or_decompress(x):
    decodings = dict()
    decodings['base16'] = lambda x: base64.b16decode(x)
    decodings['base32'] = lambda x: base64.b32decode(x)
    decodings['base58'] = lambda x: base58.b58decode(x)
    decodings['base64'] = lambda x: base64.b64decode(x)
    decodings['urlencode'] = lambda x: unquote_plus(x)
    decodings['deflate'] = lambda x: _decompress_with_zlib('deflate',  x)
    decodings['zlib'] = lambda x: _decompress_with_zlib('zlib', x)
    decodings['gzip'] = lambda x: _decompress_with_zlib('gzip', x)
    decodings['json'] = lambda x: json.loads(x)
    decodings['binary'] = lambda x: ''.join(chr(int(x[i:i+8], 2)) for i in range(0, len(x), 8))
    decodings['entity'] = lambda x: html.unescape(x)
    
    decodings['rot13'] = lambda x: codecs.decode(x, 'rot_13')
     
    try:
        lz = LZString()
        decodings['lz64'] = lambda x: lz.decompress(base64.b64decode(x).decode('utf-8'))
    except:
        pass
    
    decodings['zlib64'] = lambda x: zlib.decompress(base64.b64decode(x)).decode('utf-8', errors='ignore')
    
    try:
        lz = LZString() 
        decodings['lz64de'] = lambda x: lz.decompress(base64.b64decode(x).decode('utf-8', errors='surrogatepass'))
    except:
        pass

    try:
        lz = LZString()
        decodings['lz_string'] = lambda x: lz.decompressFromEncodedURIComponent(x)
    except:
        pass

    try: 
        import lzw
        decodings['lzw'] = lambda x: ''.join(lzw.decode(json.loads(x)))
    except:
        pass

    try:
        decodings['brotli_base64'] = lambda x: brotli.decompress(base64.b64decode(x)).decode('utf-8', errors='ignore')
    except:
        pass

    decodings['deflate_base64'] = lambda x: zlib.decompress(base64.b64decode(x), -zlib.MAX_WBITS).decode('utf-8', errors='ignore')
    decodings['deflateraw_base64'] = lambda x: zlib.decompress(base64.b64decode(x), -zlib.MAX_WBITS).decode('utf-8', errors='ignore')
    decodings['gzip_base64'] = lambda x: zlib.decompress(base64.b64decode(x), zlib.MAX_WBITS | 16).decode('utf-8', errors='ignore')
    decodings['deflate_hex'] = lambda x: zlib.decompress(bytes.fromhex(x)).decode('utf-8', errors='ignore')
    decodings['gzip_hex'] = lambda x: zlib.decompress(bytes.fromhex(x), zlib.MAX_WBITS | 16).decode('utf-8', errors='ignore')
    
    results = {}
    for name, func in decodings.items():
        try:
            result = func(x)
            results[name] = result
        except Exception as e:
            pass

    return results

def decode_or_decompress_tokens(tokens): 
    seen = set()
    results = []
    
    for item in tokens:
        if len(item) < MIN_LENGTH_OF_FIELD:
            continue
        decoded = decode_or_decompress(item)  # returns dict of {name: value}
        for value in decoded.values():
            if value is None:
                continue
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8')
                except UnicodeDecodeError:
                    value = value.hex()
            # Convert lists or dicts to string to avoid unhashable error
            if isinstance(value, (list, dict)):
                value = json.dumps(value, ensure_ascii=False)
            if value and value not in seen:
                seen.add(value)
                results.append(value)

    return results

def get_url_tokens(url):
    parsed = urlparse(url)
    tokens = set()

    # Split query into tokens
    for part in parsed.query.split('&'):
        if '=' in part:
            key, value = part.split('=', 1)
            if len(key) >= MIN_LENGTH_OF_FIELD:
                tokens.add(key)
            if len(value) >= MIN_LENGTH_OF_FIELD:
                tokens.add(value)
        elif len(part) >= MIN_LENGTH_OF_FIELD:
            tokens.add(part)

    # Extract path segments
    for segment in parsed.path.strip('/').split('/'):
        if len(segment) >= MIN_LENGTH_OF_FIELD:
            tokens.add(segment)

    # Add full URL if meaningful
    if len(url) >= MIN_LENGTH_OF_FIELD:
        tokens.add(url)

    # Add raw query string (could be base64, etc.)
    if len(parsed.query) >= MIN_LENGTH_OF_FIELD:
        tokens.add(parsed.query)
        
    return list(tokens)

def detect_leak_in_url(url):
    tokens = get_url_tokens(url)
    if not tokens:
        return None
    token_variations = decode_or_decompress_tokens(tokens) 
    matches = find_matches(MY_SENSITIVE_ENCODINGS, token_variations)
    return matches




def extract_json_tokens(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if len(str(k)) >= MIN_LENGTH_OF_FIELD:
                yield str(k)
            yield from extract_json_tokens(v)
    elif isinstance(obj, list):
        yield from extract_array_tokens(obj)
    elif isinstance(obj, (str, int, float)):
        s = str(obj)
        if len(s) >= MIN_LENGTH_OF_FIELD:
            yield s

def extract_array_tokens(arr):
    for item in arr:
        if isinstance(item, (list, tuple)):
            yield from extract_array_tokens(item)
        elif isinstance(item, dict):
            yield from extract_json_tokens(item)
        elif isinstance(item, (str, int, float)):
            s = str(item)
            if len(s) >= MIN_LENGTH_OF_FIELD:
                yield s


def get_payload_tokens(payload): 
    tokens = []  
    payload = payload.strip()
  
    if not payload:
        return tokens

    # Detect structure
    first_char = payload[0]
    tokens.append(payload)
    # If it's a JSON object
    
    
    if first_char == '{' or first_char == '[':
        try:
            decoder = json.JSONDecoder()
            idx = 0
            length = len(payload)

            def extract_json_tokens(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if len(str(k)) >= MIN_LENGTH_OF_FIELD:
                            yield str(k)
                        yield from extract_json_tokens(v)
                elif isinstance(obj, list):
                    for item in obj:
                        yield from extract_json_tokens(item)
                elif isinstance(obj, (str, int, float)):
                    s = str(obj)
                    if len(s) >= MIN_LENGTH_OF_FIELD:
                        yield s

            while idx < length:
                try:
                    obj, end = decoder.raw_decode(payload, idx)
                    tokens.extend(extract_json_tokens(obj))
                    idx = end
                    # Skip whitespace or junk between objects
                    while idx < length and payload[idx].isspace() is False and payload[idx] not in '{[':
                        idx += 1
                except json.JSONDecodeError:
                    idx += 1                
            # Recursively detect and extract from nested JSON strings
            to_remove = []
            for _ in range(6):  # Try parsing up to 5 levels deep
                additional_tokens = []
                for token in tokens: 
                    if isinstance(token, str) and token.strip().startswith(('{', '[','\n{')):
                        try:
                            nested = json.loads(token)
                            to_remove.append(token)
                            additional_tokens.extend(extract_json_tokens(nested))
                        except Exception:
                            continue
                if not additional_tokens:
                    break   
                tokens.extend(additional_tokens)
            
            tokens.extend(additional_tokens)
            tokens = list(set(tokens)) 

            for token in to_remove:
                try:
                    tokens.remove(token)
                except:
                    pass
        except Exception:
            print("Error parsing JSON object:", payload) 
            pass

    # URL-like fallback
    else:
        for part in payload.split('&'):
            if '=' in part:
                key, value = part.split('=', 1)
                if len(key) >= MIN_LENGTH_OF_FIELD:
                    tokens.append(key)
                if len(value) >= MIN_LENGTH_OF_FIELD:
                    tokens.append(value)
            elif len(part) >= MIN_LENGTH_OF_FIELD:
                tokens.append(part) 
    return [t for t in set(tokens) if len(str(t)) >= MIN_LENGTH_OF_FIELD]


def detect_leak_in_payload(payload):
    tokens = get_payload_tokens(payload)
    
    if not tokens:
        return None
    token_variations.append(payload)
    token_variations = decode_or_decompress_tokens(tokens) 
    
    token_variations = [v for v in set(token_variations) if isinstance(v, str) and len(v) >= MIN_LENGTH_OF_FIELD]
    matches = find_matches(MY_SENSITIVE_ENCODINGS, token_variations)
    return matches


 
import os
import json

FOLDER_PATH = "jsons"

def process_json_file(filepath):
    matches_found = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            #try:
            print(line_num)
            record = json.loads(line.strip())
            url = record.get("url", "")
            payload = record.get("payload", "") 

            url_tokens = get_url_tokens(url)
            payload_tokens = get_payload_tokens(payload)

            # Decode or decompress tokens
            all_tokens = url_tokens + payload_tokens
            variations = decode_or_decompress_tokens(all_tokens)
            variations.append(decode_or_decompress_tokens([payload]))
            variations.append(url)
            variations.append(payload) 
             
            
            
            site_ids = record.get("all_site_ids", "")  
            site_ids = site_ids.split(",")
            
            base_emails = [f"veli{sid.replace('_', '.')}@trustedmed.net" for sid in site_ids]
            
            # Build mail variations from base emails
            mail_variations = set()
            for email in base_emails:
                mail_variations.add(email)
                encoded = create_variations(email)
                mail_variations.update(encoded.values())

            # Copy existing encodings and add "mail"
            sensitive_encodings = {
                **MY_SENSITIVE_ENCODINGS,  # existing sensitive types
                "mail": list(mail_variations)  # new "mail" key with variations
            }
            
            # Compare against sensitive encodings
            found = find_matches(sensitive_encodings, variations)

            if found:
                matches_found.append({
                    "all_site_ids": record.get("all_site_ids", "")  ,
                    "matches": found,
                    "url": url
                })

    return matches_found

def process_all_json_files(folder_path):
    all_matches = []
    for filename in os.listdir(folder_path):
        if '.' not in filename:  # Only files with no extension
            filepath = os.path.join(folder_path, filename)
            matches = process_json_file(filepath)
            all_matches.extend(matches)

            # Save results for this file to a CSV
            if matches:
                csv_filename = os.path.join(folder_path, f"{filename}_results.csv")
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["all_site_ids", "matches", "url"])
                    writer.writeheader()
                    for row in matches:
                        writer.writerow(row)

            # Rename the file after processing
            done_path = filepath + ".done"
            os.rename(filepath, done_path)

    return all_matches# Run


def download_and_decompress_file(i):
    base_name = f"files_{i:012d}"
    local_gzip_path = os.path.join(DOWNLOAD_FOLDER, base_name + ".gzip")
    local_output_path = os.path.join(DOWNLOAD_FOLDER, base_name)

    # Skip if already processed
    if any(fname.startswith(base_name) and not fname.endswith(".gzip") for fname in os.listdir(DOWNLOAD_FOLDER)):
        print(f"[SKIP] Output already exists for: {base_name}")
        return

    file_url = f"https://storage.googleapis.com/all_urls_payloads/{base_name}.gzip"
    try:
        print(f"[DOWNLOADING] {file_url}")
        r = requests.get(file_url, stream=True)
        if r.status_code == 200:
            with open(local_gzip_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print(f"[DOWNLOADED] {base_name}.gzip")

            # Decompress
            with gzip.open(local_gzip_path, 'rb') as f_in:
                with open(local_output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"[DECOMPRESSED] → {local_output_path}")

            os.remove(local_gzip_path)
        else:
            print(f"[FAIL] Could not download {file_url}: HTTP {r.status_code}")
    except Exception as e:
        print(f"[ERROR] {base_name}: {e}")
        
        
def download_and_decompress_files():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    start, end = PROCESS_RANGE
    with multiprocessing.Pool(processes=10) as pool:
        pool.map(download_and_decompress_file, range(start, end)) 

def process_file_wrapper(filepath):
    try:
        return filepath, process_json_file(filepath)
    except Exception as e:
        print(f"[ERROR] Failed to process {filepath}: {e}")
        return filepath, []
    
def process_all_json_files(folder_path):
    all_matches = []

    files_to_process = [
        os.path.join(folder_path, fname)
        for fname in os.listdir(folder_path)
        if '.' not in fname
    ]

    with multiprocessing.Pool(processes=10) as pool:
        for filepath, file_matches in pool.imap_unordered(process_file_wrapper, files_to_process):
            all_matches.extend(file_matches)

            if file_matches:
                csv_filename = filepath + "_results.csv"
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["all_site_ids", "matches", "url"])
                    writer.writeheader()
                    for row in file_matches:
                        writer.writerow(row)

            os.rename(filepath, filepath + ".done")

    return all_matches


if __name__ == "__main__":
    download_and_decompress_files()
    matches = process_all_json_files(FOLDER_PATH)
    print(f"[DONE] Found {len(matches)} matching entries.")