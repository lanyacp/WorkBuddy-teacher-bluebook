<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>六步闭环</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>采数据 → 看得懂 → 出得准，形成可重复的循环</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'column', marginTop:16, gap:13, justifyContent:'center' }}>
    {[{n:'1',t:'学情采集',d:'表单建问卷 / AI 出题 / 扫码收数据',c:'#1A5F7A'},
      {n:'2',t:'分析与可视化',d:'一键统计 / 学情画像 / 找薄弱点',c:'#2E7D32'},
      {n:'3',t:'试卷储存与分析',d:'用 ima 个人知识库存历次试卷，长期追踪',c:'#2E7D32'},
      {n:'4',t:'错题集',d:'AI 识错 / 错因归类 / 自动成错题本',c:'#F57C00'},
      {n:'5',t:'个性化出题',d:'按薄弱点定向出题 / 一题多变',c:'#F57C00'},
      {n:'6',t:'分层作业与组卷',d:'基础 / 提高 / 拓展三层，智能组卷',c:'#C0392B'}].map((o, i) => (
      <Box key={i} style={{ flexDirection:'row', alignItems:'center', gap:14, background:'#F4F8FA', borderRadius:10, padding:'12px 18px' }}>
        <Box style={{ width:38, height:38, borderRadius:19, background:o.c, alignItems:'center', justifyContent:'center' }}>
          <Text style={{ fontSize:19, color:'#fff', fontWeight:'bold', fontFamily:'Arial' }}>{o.n}</Text>
        </Box>
        <Text style={{ fontSize:21, fontWeight:'bold', color:o.c, width:180 }}>{o.t}</Text>
        <Text style={{ fontSize:18, color:'#1F2937', flex:1 }}>{o.d}</Text>
      </Box>
    ))}
  </Box>
  <Box style={{ marginTop:12, background:'#FFF7ED', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#1F2937', textAlign:'center' }}>走到学生数据这一步，回头讲红线　——　姓名、身份证一律先脱敏</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>17 / 32</Text>
  </Box>
</Slide>
