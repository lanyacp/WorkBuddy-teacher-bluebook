<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>质量层与跨学科</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>怎么验证 AI 真的提升了掌握度，以及跨学科怎么设计</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>质量层：三个可验证的动作</Text>
      <Box style={{ marginTop:12, gap:10 }}>
        {[['前后测对比','同一知识点，AI 介入前后各测一次'],['错题追踪','同一个错因看它下次还错不错'],['目标达成度','对照教学目标逐条核对是否达成']].map((r, i) => (
          <Box key={i} style={{ background:'#FFFFFF', borderRadius:8, padding:'12px 16px' }}>
            <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>{r[0]}</Text>
            <Text style={{ fontSize:17, color:'#1F2937', marginTop:4, lineHeight:1.45 }}>{r[1]}</Text>
          </Box>
        ))}
      </Box>
      <Text style={{ fontSize:17, color:'#C0392B', marginTop:14, fontWeight:'bold', lineHeight:1.5 }}>没有验证，就只是「用过 AI」，不是「提升了」</Text>
    </Box>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#2E7D32' }}>跨学科四步设计法</Text>
      <Box style={{ marginTop:12, gap:9 }}>
        {['定一个真实问题（不是知识点，是问题）','找学科交叉点（两科在哪句话上碰到）','排任务链（每一步产出什么）','定评价证据（凭什么说学会了）'].map((s, i) => (
          <Box key={i} style={{ flexDirection:'row', gap:10, alignItems:'flex-start' }}>
            <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32', fontFamily:'Arial' }}>{i+1}</Text>
            <Text style={{ fontSize:18, color:'#1F2937', flex:1, lineHeight:1.45 }}>{s}</Text>
          </Box>
        ))}
      </Box>
      <Box style={{ marginTop:14, background:'#EAF4EA', borderRadius:8, padding:'12px 16px' }}>
        <Text style={{ fontSize:17, color:'#1F2937', lineHeight:1.5 }}>完整案例《家乡的水》（地理 + 化学 + 语文）：重点讲怎么设计，不是展示成品</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>15 / 32</Text>
  </Box>
</Slide>
