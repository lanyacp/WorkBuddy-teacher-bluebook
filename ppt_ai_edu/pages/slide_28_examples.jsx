<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>教学场景里的 Skill 例子</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>六个贴近教师日常的例子，每个都对应一个不用 Skill 时的老问题</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', flexWrap:'wrap', gap:13, marginTop:14, alignContent:'flex-start' }}>
    {[{n:'互动网页',p:'一句话生成双击即开的离线互动课件',c:'#1A5F7A'},
      {n:'微课视频',p:'讲义加素材，快速做成带配音字幕的微课',c:'#1A5F7A'},
      {n:'错题集',p:'批量上传答卷，自动生成个性化错题本',c:'#2E7D32'},
      {n:'命题组卷',p:'按知识点加难度一键组卷，含答案解析',c:'#2E7D32'},
      {n:'学情诊断',p:'成绩数据一键转成班级诊断报告',c:'#F57C00'},
      {n:'分层作业',p:'一键生成三层作业或个性化学习规划',c:'#F57C00'}].map((s, i) => (
      <Box key={i} style={{ width:'calc(33.33% - 10px)', background:'#F4F8FA', borderRadius:10, padding:'16px 18px', borderTop:'4px solid '+s.c }}>
        <Text style={{ fontSize:22, fontWeight:'bold', color:s.c }}>{s.n}</Text>
        <Text style={{ fontSize:17, color:'#1F2937', marginTop:8, lineHeight:1.55 }}>{s.p}</Text>
      </Box>
    ))}
  </Box>
  <Box style={{ marginTop:12, background:'#FFF7ED', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#1F2937', textAlign:'center' }}>注意：<span style={{ color:'#C2410C', fontWeight:'bold' }}>质量上限 = 你写的指令质量</span>　——　Skill 不是万能黑盒</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>28 / 32</Text>
  </Box>
</Slide>
