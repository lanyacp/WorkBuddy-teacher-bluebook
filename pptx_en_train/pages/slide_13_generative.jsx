<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #F57C00', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#C2410C' }}>生成性质专项：6 个译林版活动</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>开放生成统一用豆包/DeepSeek，互动呈现统一用飞象老师 —— 全程现场练出产出</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', flexWrap:'wrap', gap:14, marginTop:14, alignItems:'stretch' }}>
    {[{n:'①',t:'协同写作：推荐信',u:'九上U1 Know yourself',w:'豆包/DeepSeek',c:'#1A5F7A'},
      {n:'②',t:'故事续写：Down the rabbit hole',u:'七下U8 Wonderland',w:'豆包 → 飞象展览',c:'#2E7D32'},
      {n:'③',t:'角色对话创编：邻里',u:'七下U2 Neighbourhoods',w:'飞象/豆包',c:'#1A5F7A'},
      {n:'④',t:'家乡变化双语海报',u:'八下U1 Past and present',w:'豆包 → 飞象海报',c:'#C2410C'},
      {n:'⑤',t:'词汇生成游戏：种小树/翻牌',u:'七上U2 / 七上U7',w:'飞象老师',c:'#1A5F7A'},
      {n:'⑥',t:'读书短剧脚本 + 分镜',u:'八下U4 / 九上U8',w:'豆包 → 飞象配音',c:'#2E7D32'}].map((a, i) => (
      <Box key={i} style={{ width:'calc(33.33% - 10px)', background:'#F4F8FA', borderRadius:12, padding:'16px 18px', borderTop:'4px solid '+a.c, justifyContent:'space-between' }}>
        <Box style={{ flexDirection:'row', alignItems:'center', gap:10 }}>
          <Box style={{ width:34, height:34, borderRadius:17, background:a.c, alignItems:'center', justifyContent:'center' }}><Text style={{ fontSize:17, color:'#fff', fontWeight:'bold' }}>{a.n}</Text></Box>
          <Text style={{ fontSize:19, fontWeight:'bold', color:'#1F2937' }}>{a.t}</Text>
        </Box>
        <Box style={{ marginTop:10 }}>
          <Text style={{ fontSize:15, color:'#5B6B7B' }}>真实单元：{a.u}</Text>
          <Box style={{ marginTop:8, background:'#FFFFFF', borderRadius:6, padding:'6px 10px' }}><Text style={{ fontSize:14, color:a.c, fontWeight:'bold' }}>工具：{a.w}</Text></Box>
        </Box>
      </Box>
    ))}
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI 赋能英语教学 · 课标锚定版</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>13 / 15</Text>
  </Box>
</Slide>
