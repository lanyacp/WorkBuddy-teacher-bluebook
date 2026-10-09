<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #C0392B', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#C0392B' }}>痛点共鸣</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>先说我们为什么来，两件事</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 24px' }}>
      <Text style={{ fontSize:24, fontWeight:'bold', color:'#1A5F7A' }}>一、老师的时间去哪了</Text>
      <Box style={{ marginTop:14, gap:10 }}>
        {[['备课','一节公开课磨两天'],['批改','两个班改到半夜'],['找题','翻资料翻一周'],['做材料','PPT 做到凌晨']].map((r, i) => (
          <Box key={i} style={{ flexDirection:'row', alignItems:'center', background:'#FFFFFF', borderRadius:8, padding:'11px 16px' }}>
            <Text style={{ fontSize:20, fontWeight:'bold', color:'#1A5F7A', width:110 }}>{r[0]}</Text>
            <Text style={{ fontSize:18, color:'#1F2937' }}>{r[1]}</Text>
          </Box>
        ))}
      </Box>
      <Text style={{ fontSize:18, color:'#C0392B', marginTop:14, fontWeight:'bold' }}>这些活里，有一半是重复劳动</Text>
    </Box>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 24px' }}>
      <Text style={{ fontSize:24, fontWeight:'bold', color:'#1A5F7A' }}>二、县域教师三重困境</Text>
      <Box style={{ marginTop:14, gap:10 }}>
        {[['没人带','想学但不知道从哪学起'],['资源少','没有像样的教研与培训'],['怕担责','想用又怕出问题']].map((r, i) => (
          <Box key={i} style={{ flexDirection:'row', alignItems:'center', background:'#FFFFFF', borderRadius:8, padding:'13px 16px' }}>
            <Text style={{ fontSize:20, fontWeight:'bold', color:'#C0392B', width:110 }}>{r[0]}</Text>
            <Text style={{ fontSize:18, color:'#1F2937' }}>{r[1]}</Text>
          </Box>
        ))}
      </Box>
      <Text style={{ fontSize:18, color:'#C0392B', marginTop:14, fontWeight:'bold' }}>第三条最真实，今天要正面解决</Text>
    </Box>
  </Box>
  <Box style={{ marginTop:14, background:'#FCEBEA', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#7F1D1D', textAlign:'center' }}>现在举手：怕担责的请举手　——　第三种困境，通常是举手最多的</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>05 / 32</Text>
  </Box>
</Slide>
