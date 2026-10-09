<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #C0392B', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#C0392B' }}>数据安全三条红线</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>只有 10 分钟，但每一条都不能破。这是全场唯一必须讲的内容</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:16, marginTop:16, alignItems:'stretch' }}>
    {[{n:'1',t:'学生隐私数据不上传',d:'姓名、身份证、住址、电话先脱敏，用「学生 A / 学生 B / 班级 1」代替。\n\n录课堂音视频前，要先向学生与监护人说明并取得单独授权。'},
      {n:'2',t:'AI 输出必须人工复核',d:'批改、评语、试题、分析结论都要老师把关。\n\nAI 给的是草稿，出问题签字的是你。责任不会转移给工具。'},
      {n:'3',t:'成文内容标注 AI 参与',d:'论文、课题、案例如实说明 AI 辅助情况。\n\n核心论点与论证过程必须自己完成，不能直接提交生成内容。'}].map((o, i) => (
      <Box key={i} style={{ flex:1, background:'#FCEBEA', borderRadius:12, padding:'22px 24px', borderTop:'5px solid #C0392B' }}>
        <Text style={{ fontSize:52, fontWeight:'bold', color:'#C0392B', fontFamily:'Arial' }}>{o.n}</Text>
        <Text style={{ fontSize:25, fontWeight:'bold', color:'#1F2937', marginTop:8 }}>{o.t}</Text>
        <Text style={{ fontSize:18, color:'#5B6B7B', marginTop:14, lineHeight:1.65 }}>{o.d}</Text>
      </Box>
    ))}
  </Box>
  <Box style={{ marginTop:16, background:'#F4F8FA', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#1F2937', textAlign:'center' }}>这三条会在讲到学生信息、评语批改、论文写作时反复回扣　——　提示卡已发到手</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>10 / 32</Text>
  </Box>
</Slide>
