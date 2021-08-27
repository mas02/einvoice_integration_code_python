
host = 'https://api.mastersindia.co'
certificate = 'qa_certs/qa_server.crt'
gstr_urls = {
    'ACCESS_TOKEN' : host + '/oauth/access_token',
    'auth_url' : host + '/eivital/v1.04/auth',
    'gen_einv' :host + '/eicore/v1.03/Invoice',
    'cancel_einv' : host + '/eicore/v1.03/Invoice/Cancel',
    'get_einv' : host + '/eicore/v1.03/Invoice/irn/',
    'CERIFICATE_PATH': certificate
}

GstinInfo={     
    'gstin':'',
    'einv_username':'',
    'einv_password':''
    
}

data_json = '{"Version":"1.1","TranDtls":{"TaxSch":"GST","SupTyp":"B2B","RegRev":"N","IgstOnIntra":"N"},"DocDtls":{"Typ":"INV","No":"Test/IRNGV","Dt":"08\/03\/2021"},"SellerDtls":{"Gstin":"09AAAPG7885R002","LglNm":"Colorshine Coated Private Limi","TrdNm":"Colorshine Coated Private Limi","Addr1":"1229 - 1, 1230 -2Chennuru Bit - 1 villageGuduru Mandal","Addr2":"1229 - 1, 1230 -2Chennuru Bit - 1 villageGuduru Mandal","Loc":"Manesar","Pin":201301,"Stcd":"09","Ph":"9100090540","Em":"corporate@colorshine.net"},"BuyerDtls":{"Gstin":"05AAAPG7885R002","LglNm":"Century Wells Roofing India Pv","TrdNm":"Century Wells Roofing India Pv","Addr1":"No 219A, Bommasandra Industrial AreaSurvey No 19( Part) 35 And 36Bommasadra Villege Attibele Hobli,","Loc":"Gurgaon","Pin":263001,"Pos":"05","Stcd":"05"},"DispDtls":{"Nm":"Century Wells Roofing India Pv","Addr1":"No 219A, Bommasandra Industrial AreaSurvey No 19( Part) 35 And 36Bommasadra Villege Attibele Hobli,","Loc":"Manesar","Pin":122050,"Stcd":"06"},"ShipDtls":{"Gstin":"06AAACA7205Q1ZK","LglNm":"Colorshine Coated Private Limi","TrdNm":"Colorshine Coated Private Limi","Addr1":"1229 - 1, 1230 -2Chennuru Bit - 1 villageGuduru Mandal","Loc":"Gurgaon","Pin":122001,"Stcd":"06"},"ValDtls":{"AssVal":613258.68,"CgstVal":0,"SgstVal":0,"IgstVal":110386.56,"CesVal":0,"StCesVal":0,"Discount":0,"OthChrg":0,"RndOffAmt":0,"TotInvVal":723645.24,"TotInvValFc":12897.7},"ItemList":[{"SlNo":"1","PrdDesc":"COLORSHINE PRATHAM PPGI COIL","IsServc":"N","HsnCd":"721011","Barcde":"123456","Qty":4.015,"Unit":"MTS","UnitPrice":77194,"TotAmt":309933.91,"Discount":0,"PreTaxVal":0,"AssAmt":309933.91,"GstRt":18,"IgstAmt":55788.1,"CgstAmt":0,"SgstAmt":0,"CesRt":0,"CesAmt":0,"CesNonAdvlAmt":0,"StateCesRt":0,"StateCesAmt":0,"StateCesNonAdvlAmt":0,"OthChrg":0,"TotItemVal":365722.01},{"SlNo":"2","PrdDesc":"COLORSHINE PRATHAM PPGI COIL","IsServc":"N","HsnCd":"721011","Barcde":"123456","Qty":3.955,"Unit":"MTS","UnitPrice":76694,"TotAmt":303324.77,"Discount":0,"PreTaxVal":0,"AssAmt":303324.77,"GstRt":18,"IgstAmt":54598.46,"CgstAmt":0,"SgstAmt":0,"CesRt":0,"CesAmt":0,"CesNonAdvlAmt":0,"StateCesRt":0,"StateCesAmt":0,"StateCesNonAdvlAmt":0,"OthChrg":0,"TotItemVal":357923.23}]}'


cancel_irn_json = '{"Irn":"0657ea66f6461c473a05754b5cdee3531032924fe81635a6433fdd9313125b1b","CnlRsn":"1","CnlRem":"Wrong entry"}'


accessTokenInfo={    
    'username' :'',
    'password' :'',
    'client_id' :'',
    'client_secret' :'',
    'grant_type' : 'password'
}

