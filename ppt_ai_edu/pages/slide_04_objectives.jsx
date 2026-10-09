<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>学习目标</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>今天不讲工具清单，只讲四件你能带走的事</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', flexWrap:'wrap', gap:16, marginTop:14 }}>
    {[{n:'会提问',t:'能写出一条完整提示词',d:'说清角色、任务、要求三要素，抄学员手册的模板就能用',c:'#1A5F7A'},
      {n:'会应用',t:'能用 AI 产出一份真实材料',d:'教案、学情问卷、错题本、评语，至少一样真的做出来',c:'#2E7D32'},
      {n:'会沉淀',t:'能把重复流程写成模板',d:'骨干学员能交出一个自建 Skill，一个人建好全组受益',c:'#F57C00'},
      {n:'会判断',t:'能识别 AI 输出哪里不对',d:'知道哪些必须人工复核，哪些根本不能用',c:'#C0392B'}].map((o, i) => (
      <Box key={i} style={{ width:'calc(50% - 8px)', height:'calc(50% - 8px)', background:'#F4F8FA', borderRadius:12, padding:'20px 24px', borderLeft:'6px solid '+o.c, justifyContent:'center' }}>
        <Text style={{ fontSize:34, fontWeight:'bold', color:o.c }}>{o.n}</Text>
        <Text style={{ fontSize:22, fontWeight:'bold', color:'#1F2937', marginTop:6 }}>{o.t}</Text>
        <Text style={{ fontSize:18, color:'#5B6B7B', marginTop:8, lineHeight:1.5 }}>{o.d}</Text>
      </Box>
    ))}
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>04 / 32</Text>
  </Box>
</Slide>
