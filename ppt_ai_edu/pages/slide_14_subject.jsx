<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>学科层：五科各一个 AI 设计点</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>按你教的学科挑一到两个讲透，不要五科都讲一遍</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', flexWrap:'wrap', gap:13, marginTop:14, alignContent:'flex-start' }}>
    {[{n:'语文',d:'阅读与写作：AI 出导读问题链，帮你把「读懂了吗」变成可检验的问题',c:'#C0392B'},
      {n:'数学',d:'概念与推演：AI 生成多角度例题，暴露学生可能的错误路径',c:'#1A5F7A'},
      {n:'英语',d:'听说情境：用 AI 角色扮演做陪练，生成听说任务与情境对话',c:'#2E7D32'},
      {n:'理化',d:'实验与探究：AI 帮你设计变量控制表与实验记录单',c:'#F57C00'},
      {n:'政史',d:'史料与情境：AI 把时事材料改写成学生能代入的情境问题',c:'#7B3F9D'}].map((s, i) => (
      <Box key={i} style={{ width:'calc(33.33% - 10px)', background:'#F4F8FA', borderRadius:10, padding:'16px 18px', borderLeft:'5px solid '+s.c }}>
        <Text style={{ fontSize:23, fontWeight:'bold', color:s.c }}>{s.n}</Text>
        <Text style={{ fontSize:17, color:'#1F2937', marginTop:8, lineHeight:1.55 }}>{s.d}</Text>
      </Box>
    ))}
    <Box style={{ width:'calc(33.33% - 10px)', background:'#FFF7ED', borderRadius:10, padding:'16px 18px', borderLeft:'5px solid #F57C00' }}>
      <Text style={{ fontSize:19, fontWeight:'bold', color:'#C2410C' }}>讲法提醒</Text>
      <Text style={{ fontSize:17, color:'#1F2937', marginTop:8, lineHeight:1.55 }}>每个学科 3 分钟过一遍即可，重点留给你自己那科</Text>
    </Box>
  </Box>
  <Box style={{ marginTop:14, background:'#F4F8FA', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#1F2937', textAlign:'center' }}>课前请想好：我要给你们科的老师讲哪一个案例</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>14 / 32</Text>
  </Box>
</Slide>
