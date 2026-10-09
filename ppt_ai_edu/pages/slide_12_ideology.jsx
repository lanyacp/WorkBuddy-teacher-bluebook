<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>理念层与大单元</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>从知识灌输到素养立意，让教材从零散走向结构化</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>从知识灌输到素养立意</Text>
      <Box style={{ marginTop:12, gap:10 }}>
        {[['过去','按课时推进，讲完一课算一课'],['现在','指向核心素养，评价方式跟着变']].map((r, i) => (
          <Box key={i} style={{ background:'#FFFFFF', borderRadius:8, padding:'12px 16px' }}>
            <Text style={{ fontSize:16, color:'#F57C00', fontWeight:'bold' }}>{r[0]}</Text>
            <Text style={{ fontSize:18, color:'#1F2937', marginTop:4 }}>{r[1]}</Text>
          </Box>
        ))}
      </Box>
      <Text style={{ fontSize:17, color:'#5B6B7B', marginTop:14, lineHeight:1.6 }}>把一节课放进单元里看，才知道它该服务于哪个终点。</Text>
    </Box>
    <Box style={{ flex:1.2, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#2E7D32' }}>大单元 / 大概念怎么用 AI 排</Text>
      <Box style={{ marginTop:12, gap:9 }}>
        {['先定这个单元要培养的核心能力','再拆成 3-4 个子任务，标出前后逻辑关系','给每个子任务设计一个可检验的产出','最后确认哪些环节 AI 能帮，哪些必须你来定'].map((s, i) => (
          <Box key={i} style={{ flexDirection:'row', gap:10, alignItems:'flex-start' }}>
            <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32', fontFamily:'Arial' }}>{i+1}</Text>
            <Text style={{ fontSize:18, color:'#1F2937', flex:1, lineHeight:1.45 }}>{s}</Text>
          </Box>
        ))}
      </Box>
      <Box style={{ marginTop:14, background:'#EAF4EA', borderRadius:8, padding:'12px 16px' }}>
        <Text style={{ fontSize:17, color:'#1F2937', lineHeight:1.5 }}>现场任务：给你的单元画一张结构图，画完再让 AI 挑毛病。</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>12 / 32</Text>
  </Box>
</Slide>
