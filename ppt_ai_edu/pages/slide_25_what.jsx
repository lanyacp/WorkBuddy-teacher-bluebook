<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>什么是 Skill</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>一句话触发的封装流程。三个类比，听完就懂</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'column', marginTop:16, gap:13, justifyContent:'center' }}>
    <Box style={{ background:'#1A5F7A', borderRadius:12, padding:'20px 26px' }}>
      <Text style={{ fontSize:21, fontWeight:'bold', color:'#FFFFFF' }}>定义</Text>
      <Text style={{ fontSize:19, color:'#CFE3EA', marginTop:8, lineHeight:1.6 }}>Skill 是把一套固定步骤、标准化流程，封装成「一句话触发」的能力模块。</Text>
    </Box>
    <Box style={{ flexDirection:'row', gap:13 }}>
      {[['菜谱','vs 预制菜','散装的方法论', 'vs 封装好的方法论'],
        ['一次性提醒','vs 每天响的闹钟','这次要交代', 'vs 以后都按这个来'],
        ['临时找人帮忙','vs 请了固定助手','每次找人', 'vs 一直有人']].map((r, i) => (
        <Box key={i} style={{ flex:1, background:'#F4F8FA', borderRadius:10, padding:'16px 18px' }}>
          <Text style={{ fontSize:18, color:'#1F2937', fontWeight:'bold' }}>{r[0]}</Text>
          <Text style={{ fontSize:15, color:'#94A3B8', marginTop:2 }}>{r[1]}</Text>
          <Text style={{ fontSize:17, color:'#5B6B7B', marginTop:8, lineHeight:1.5 }}>{r[2]}</Text>
          <Text style={{ fontSize:15, color:'#94A3B8', marginTop:2 }}>{r[3]}</Text>
        </Box>
      ))}
    </Box>
  </Box>
  <Box style={{ marginTop:14, background:'#EAF4EA', borderRadius:10, padding:'14px 20px' }}>
    <Text style={{ fontSize:19, color:'#1F2937', textAlign:'center' }}>用类比复述一遍：提示词解决<span style={{ color:'#2E7D32', fontWeight:'bold' }}>这一次怎么说</span>，Skill 解决<span style={{ color:'#2E7D32', fontWeight:'bold' }}>这一类以后都怎么做</span></Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>25 / 32</Text>
  </Box>
</Slide>
