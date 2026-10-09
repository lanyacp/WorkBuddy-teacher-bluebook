<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>三步走：找装 → 触发 → 微调</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>现场走一遍，你就知道该在哪一步花时间</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'column', marginTop:16, gap:13, justifyContent:'center' }}>
    {[{n:'第 1 步',t:'找 / 装',d:'在技能市场搜索你学科的技能，一键安装。11 大类教师技能，按学科找。',c:'#1A5F7A'},
      {n:'第 2 步',t:'触发',d:'用一句自然语言指令触发。要素 = 学科 + 年级 + 教材版本 + 单元/主题 + 数量难度 + 产出格式。',c:'#2E7D32'},
      {n:'第 3 步',t:'微调',d:'产出后对话修改，比如「选择题增加到 10 道」，确认后再导出。',c:'#F57C00'}].map((o, i) => (
      <Box key={i} style={{ flexDirection:'row', alignItems:'center', gap:16, background:'#F4F8FA', borderRadius:12, padding:'18px 22px' }}>
        <Box style={{ width:92, alignItems:'center' }}>
          <Text style={{ fontSize:17, color:'#94A3B8' }}>{o.n}</Text>
        </Box>
        <Box style={{ width:110, background:o.c, borderRadius:8, padding:'12px 0', alignItems:'center' }}>
          <Text style={{ fontSize:24, fontWeight:'bold', color:'#FFFFFF' }}>{o.t}</Text>
        </Box>
        <Text style={{ fontSize:19, color:'#1F2937', flex:1, lineHeight:1.5 }}>{o.d}</Text>
      </Box>
    ))}
  </Box>
  <Box style={{ marginTop:12, background:'#1F2937', borderRadius:10, padding:'14px 20px' }}>
    <Text style={{ fontSize:18, color:'#E5E7EB', textAlign:'center' }}>触发指令模板：学科 &lt;学科&gt; ｜ 年级 &lt;年级&gt; ｜ 版本 &lt;教材版本&gt; ｜ 单元 &lt;单元/主题&gt; ｜ 数量难度 &lt;数量与难度&gt; ｜ 产出 &lt;格式&gt;</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>27 / 32</Text>
  </Box>
</Slide>
