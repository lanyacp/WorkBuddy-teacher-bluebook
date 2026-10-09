<Slide style={{ width:'1280px', height:'720px', background:'linear-gradient(135deg,#2E7D32 0%, #1A5F7A 100%)', display:'flex', flexDirection:'column', justifyContent:'center', padding:'0 90px' }}>
  <Text style={{ fontSize:22, color:'#D5EBD9', letterSpacing:4, fontWeight:'bold' }}>板块二　P31 - P46</Text>
  <Text style={{ fontSize:56, fontWeight:'bold', color:'#FFFFFF', marginTop:14 }}>学情闭环</Text>
  <Text style={{ fontSize:26, color:'#EAF3F6', marginTop:14 }}>采集 → 分析 → 错题 → 出题 → 分层 → 组卷</Text>
  <Box style={{ width:100, height:4, background:'#F57C00', marginTop:24, marginBottom:24 }} />
  <Box style={{ flexDirection:'row', gap:12 }}>
    {['学情采集','分析可视化','试卷储存','错题集','个性化出题','分层作业'].map((s, i) => (
      <Box key={i} style={{ background:'rgba(255,255,255,0.16)', padding:'11px 18px', borderRadius:8 }}><Text style={{ color:'#fff', fontSize:18 }}>{s}</Text></Box>
    ))}
  </Box>
  <Text style={{ fontSize:20, color:'#D5EBD9', marginTop:28 }}>这是全场最容易出成果的一个板块，务必留足实操时间</Text>
</Slide>
