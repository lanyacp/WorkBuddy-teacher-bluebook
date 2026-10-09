<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>提示词公式</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>全场最重要的一页。后面每个板块都靠它，砍了后面全废</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'column', marginTop:14, gap:14 }}>
    <Box style={{ flexDirection:'row', gap:12 }}>
      {[['角色','你是一位有 10 年教龄的初中英语教师','#1A5F7A'],
        ['任务','请帮我为七年级设计一份 Unit 1 写作任务','#2E7D32'],
        ['要求','80 词左右，含 3 个可替换点，用初中词汇','#F57C00']].map((r, i) => (
        <Box key={i} style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'18px 20px', borderTop:'5px solid '+r[2] }}>
          <Text style={{ fontSize:26, fontWeight:'bold', color:r[2] }}>{r[0]}</Text>
          <Text style={{ fontSize:18, color:'#1F2937', marginTop:10, lineHeight:1.5 }}>{r[1]}</Text>
        </Box>
      ))}
    </Box>
    <Box style={{ background:'#1F2937', borderRadius:12, padding:'18px 22px' }}>
      <Text style={{ fontSize:19, color:'#9CA3AF' }}>完整示例</Text>
      <Text style={{ fontSize:21, color:'#E5E7EB', marginTop:8, lineHeight:1.6 }}>你是一位有 10 年教龄的初中英语教师。请帮我为七年级设计一份 Unit 1 写作任务。要求 80 词左右，含 3 个可替换点，用初中词汇。</Text>
    </Box>
    <Box style={{ flexDirection:'row', gap:12, flex:1 }}>
      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'14px 18px' }}>
        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>追问细化</Text>
        <Text style={{ fontSize:17, color:'#1F2937', marginTop:6, lineHeight:1.5 }}>太简单了，改成每项配 2-3 句示例</Text>
      </Box>
      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'14px 18px' }}>
        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>给范例</Text>
        <Text style={{ fontSize:17, color:'#1F2937', marginTop:6, lineHeight:1.5 }}>照这个格式再写一份：附上你已认可的一段</Text>
      </Box>
      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'14px 18px' }}>
        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>限定输出</Text>
        <Text style={{ fontSize:17, color:'#1F2937', marginTop:6, lineHeight:1.5 }}>用表格输出，每题标注难度与知识点</Text>
      </Box>
      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'14px 18px' }}>
        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>让它自检</Text>
        <Text style={{ fontSize:17, color:'#1F2937', marginTop:6, lineHeight:1.5 }}>写完自查有没有超纲，并标出存疑处</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>09 / 32</Text>
  </Box>
</Slide>
