<Slide style={{ width:'1280px', height:'720px', background:'linear-gradient(135deg,#1A5F7A 0%, #4A3A6B 100%)', display:'flex', flexDirection:'column', justifyContent:'center', padding:'0 90px' }}>
  <Text style={{ fontSize:22, color:'#CFE3EA', letterSpacing:4, fontWeight:'bold' }}>板块三　P47 - P58</Text>
  <Text style={{ fontSize:56, fontWeight:'bold', color:'#FFFFFF', marginTop:14 }}>教研与专业成长</Text>
  <Text style={{ fontSize:26, color:'#EAF3F6', marginTop:14 }}>县域教师最刚需的一块：把 AI 嵌进研修，也写进论文与职称</Text>
  <Box style={{ width:100, height:4, background:'#F57C00', marginTop:24, marginBottom:24 }} />
  <Box style={{ flexDirection:'row', gap:12 }}>
    {['校本研修','集体备课','听课评课','设计打磨','论文写作','课题职称'].map((s, i) => (
      <Box key={i} style={{ background:'rgba(255,255,255,0.16)', padding:'11px 18px', borderRadius:8 }}><Text style={{ color:'#fff', fontSize:18 }}>{s}</Text></Box>
    ))}
  </Box>
  <Text style={{ fontSize:20, color:'#CFE3EA', marginTop:28 }}>超时优先砍这一块，砍掉不影响学员获得感</Text>
</Slide>
