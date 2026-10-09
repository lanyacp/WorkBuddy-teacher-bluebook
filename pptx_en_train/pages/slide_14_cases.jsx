<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #C0392B', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#C0392B' }}>一线案例与 6 大痛点（禅城区 7 校）</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>真实痛点 + 真实做法，逐条对齐 16 法与译林版单元</Text>
  </Box>
  <Box style={{ marginTop:12 }}>
    <Text style={{ fontSize:17, fontWeight:'bold', color:'#1A5F7A', marginBottom:8 }}>7 校实践来源</Text>
    <Box style={{ flexDirection:'row', flexWrap:'wrap', gap:8 }}>
      {['佛大附校 招蔼珊/孙雅琪','市实验 杨小红','澜石中学 罗浩','第十中学 黄家裕','佛外学校 罗彩甜','城北中学 罗艳君/潘春燕','佛外高中部 徐佳岚/游伟仪'].map((s, i) => (
        <Box key={i} style={{ background:'#F4F8FA', borderRadius:16, padding:'6px 14px' }}><Text style={{ fontSize:15, color:'#1F2937' }}>{s}</Text></Box>
      ))}
    </Box>
  </Box>
  <Box style={{ flex:1, marginTop:14, gap:9 }}>
    {[{p:'讲评课学生被动走神',q:'"讲完形我讲得口干，学生该睡的睡。"',u:'八上U1 / 七下U8'},
      {p:'词汇听默单调',q:'"单词听写学生恨，我也恨。"',u:'七上U2 / 七上U7'},
      {p:'早读不敢开口',q:'"齐读像念经，个别抽问一片沉默。"',u:'七上U1 / 八上U1'},
      {p:'写作结构记不住',q:'"背模板也写不出像样的信。"',u:'九上U1 推荐信'},
      {p:'语法备课翻倍',q:'"比较级+最高级 5 课时，资料翻一周。"',u:'八上U1 / 九上U1'},
      {p:'听力检测难兼顾趣味',q:'"听力测验像在考纪律。"',u:'八上U5 / 七下U5'}].map((x, i) => (
      <Box key={i} style={{ flexDirection:'row', alignItems:'center', gap:12, background:'#FCEBEA', borderRadius:8, padding:'9px 14px' }}>
        <Text style={{ fontSize:18, fontWeight:'bold', color:'#C0392B', fontFamily:'Arial' }}>{i+1}</Text>
        <Text style={{ fontSize:17, color:'#1F2937', fontWeight:'bold', width:230 }}>{x.p}</Text>
        <Text style={{ fontSize:16, color:'#7F1D1D', fontStyle:'italic', flex:1 }}>{x.q}</Text>
        <Text style={{ fontSize:14, color:'#9A3412' }}>{x.u}</Text>
      </Box>
    ))}
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI 赋能英语教学 · 课标锚定版</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>14 / 15</Text>
  </Box>
</Slide>
