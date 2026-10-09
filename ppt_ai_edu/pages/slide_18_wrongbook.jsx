<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>错题集：把错题变成资产</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>AI 识错 → 错因归类 → 自动成错题本（学生版 / 班级版）</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>错因标签是抓手</Text>
      <Text style={{ fontSize:17, color:'#5B6B7B', marginTop:6 }}>不给标签，AI 只能「对答案」；给了标签，才能分析</Text>
      <Box style={{ flexDirection:'row', flexWrap:'wrap', gap:9, marginTop:14 }}>
        {['生词','搭配','逻辑','时态','审题','书写'].map((s, i) => (
          <Box key={i} style={{ background:'#FFFFFF', borderRadius:16, padding:'8px 18px', border:'1px solid #C0392B' }}>
            <Text style={{ fontSize:19, color:'#C0392B', fontWeight:'bold' }}>{s}</Text>
          </Box>
        ))}
      </Box>
      <Text style={{ fontSize:18, color:'#1F2937', marginTop:16, lineHeight:1.6 }}>一个错题集做完，还能顺手做两件事：按标签统计高频错因，针对性出变式题。</Text>
    </Box>
    <Box style={{ flex:1, background:'#1F2937', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:19, color:'#FBBF24', fontWeight:'bold' }}>提示词（改尖括号即可用）</Text>
      <Text style={{ fontSize:18, color:'#E5E7EB', marginTop:12, lineHeight:1.7 }}>你是一位&lt;学科&gt;教师。这是我们班最近的&lt;份数&gt;份错题。请按错因分类（生词 / 搭配 / 逻辑 / 时态 / 审题 / 书写），统计各类的题量与占比，指出最该优先解决的三类，并针对最高频的那一类出 3 道变式题。</Text>
      <Box style={{ marginTop:14, borderTop:'1px solid #374151', paddingTop:10 }}>
        <Text style={{ fontSize:16, color:'#9CA3AF', fontStyle:'italic' }}>提醒：错题内容也含学生隐私，贴之前先脱敏，用学生 A / B 代替。</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>18 / 32</Text>
  </Box>
</Slide>
