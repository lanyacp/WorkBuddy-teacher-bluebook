<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>免费工具地图</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>8 款够用了。每个工具只讲一个最常用场景，不要贪多</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', flexWrap:'wrap', gap:13, marginTop:14, alignContent:'flex-start' }}>
    {[{n:'DeepSeek',s:'对话大模型',u:'网页版，浏览器直接开',c:'#1A5F7A'},
      {n:'豆包',s:'对话大模型',u:'手机 App，随时问答',c:'#1A5F7A'},
      {n:'腾讯元宝',s:'对话大模型',u:'微信小程序',c:'#1A5F7A'},
      {n:'腾讯 ima',s:'个人知识库',u:'存试卷、建错题库',c:'#2E7D32'},
      {n:'Kimi',s:'长文本',u:'读整本教材单元',c:'#2E7D32'},
      {n:'问卷工具',s:'表单收集',u:'学情问卷、家长回执',c:'#2E7D32'},
      {n:'扣子 Coze',s:'工作流',u:'批量自动化，进阶',c:'#F57C00'},
      {n:'WorkBuddy',s:'桌面客户端',u:'Skill 技能，板块五核心',c:'#F57C00'}].map((t, i) => (
      <Box key={i} style={{ width:'calc(25% - 10px)', background:'#F4F8FA', borderRadius:10, padding:'14px 16px', borderTop:'4px solid '+t.c }}>
        <Text style={{ fontSize:22, fontWeight:'bold', color:t.c }}>{t.n}</Text>
        <Text style={{ fontSize:16, color:'#1F2937', marginTop:6 }}>{t.s}</Text>
        <Text style={{ fontSize:15, color:'#5B6B7B', marginTop:4 }}>{t.u}</Text>
      </Box>
    ))}
  </Box>
  <Box style={{ marginTop:12, background:'#FFF7ED', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#1F2937', textAlign:'center' }}>建议只挑 <span style={{ color:'#C2410C', fontWeight:'bold' }}>2 样</span> 用熟 21 天。全学一遍，等于一个都没学会</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>08 / 32</Text>
  </Box>
</Slide>
