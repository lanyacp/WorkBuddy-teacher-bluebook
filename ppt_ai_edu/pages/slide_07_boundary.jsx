<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>AI 能做什么，不能做什么</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>先划边界，再谈用法。这一页能省掉你很多焦虑</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#EAF4EA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:23, fontWeight:'bold', color:'#2E7D32' }}>能做，而且做得快</Text>
      <Box style={{ marginTop:12, gap:9 }}>
        {['大量重复性的文字工作（教案、评语、通知）','按模板批量生成（试题、练习、变式）','整理归纳（错题归类、成绩分析、资料汇总）','提供多版本供你挑选对比','陪你练口语、随时提问'].map((s, i) => (
          <Box key={i} style={{ flexDirection:'row', gap:9, alignItems:'flex-start' }}>
            <Text style={{ fontSize:15, color:'#2E7D32', fontWeight:'bold' }}>✓</Text>
            <Text style={{ fontSize:18, color:'#1F2937', flex:1, lineHeight:1.45 }}>{s}</Text>
          </Box>
        ))}
      </Box>
    </Box>
    <Box style={{ flex:1, background:'#FCEBEA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:23, fontWeight:'bold', color:'#C0392B' }}>做不了，也别交给它</Text>
      <Box style={{ marginTop:12, gap:9 }}>
        {['替你判断学生到底学会了没有','替你做价值引领和情感沟通','保证事实正确、保证不超纲','替你承担责任（签字的是你）','处理未脱敏的学生隐私数据'].map((s, i) => (
          <Box key={i} style={{ flexDirection:'row', gap:9, alignItems:'flex-start' }}>
            <Text style={{ fontSize:15, color:'#C0392B', fontWeight:'bold' }}>✕</Text>
            <Text style={{ fontSize:18, color:'#1F2937', flex:1, lineHeight:1.45 }}>{s}</Text>
          </Box>
        ))}
      </Box>
    </Box>
  </Box>
  <Box style={{ marginTop:14, background:'#F4F8FA', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#1F2937', textAlign:'center' }}>AI 始终是助手，育人主体永远是老师　——　这句话出自《教师生成式人工智能应用指引》</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>07 / 32</Text>
  </Box>
</Slide>
