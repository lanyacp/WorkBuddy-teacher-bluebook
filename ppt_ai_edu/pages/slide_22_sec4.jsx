<Slide style={{ width:'1280px', height:'720px', background:'linear-gradient(135deg,#F57C00 0%, #C0392B 100%)', display:'flex', flexDirection:'column', justifyContent:'center', padding:'0 90px' }}>
  <Text style={{ fontSize:22, color:'#FDEBD0', letterSpacing:4, fontWeight:'bold' }}>板块四　P59 - P69</Text>
  <Text style={{ fontSize:56, fontWeight:'bold', color:'#FFFFFF', marginTop:14 }}>学生管理与家校协同</Text>
  <Text style={{ fontSize:26, color:'#FEF3E2', marginTop:14 }}>班主任与科任教师的日常，最碎也最耗时</Text>
  <Box style={{ width:100, height:4, background:'#FFFFFF', marginTop:24, marginBottom:24 }} />
  <Box style={{ flexDirection:'row', gap:12 }}>
    {['班会设计','批量评语','家长会材料','分场景话术','成长档案','班级数据','特殊学生'].map((s, i) => (
      <Box key={i} style={{ background:'rgba(255,255,255,0.18)', padding:'11px 18px', borderRadius:8 }}><Text style={{ color:'#fff', fontSize:18 }}>{s}</Text></Box>
    ))}
  </Box>
  <Text style={{ fontSize:20, color:'#FDEBD0', marginTop:28 }}>非班主任班可把家校部分合并讲，重点放合规与班级数据</Text>
</Slide>
