<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>学习路径图</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>把单元从「起点」画到「终点证据」，每级台阶标明怎么检验</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'column', marginTop:16, gap:14 }}>
    <Box style={{ flexDirection:'row', alignItems:'center', gap:0, flex:1 }}>
      {[{s:'起点',d:'学生现在会什么',c:'#94A3B8'},
        {s:'台阶一',d:'概念理解',c:'#1A5F7A'},
        {s:'台阶二',d:'基本应用',c:'#2E7D32'},
        {s:'台阶三',d:'迁移与探究',c:'#F57C00'},
        {s:'终点',d:'可检验的产出证据',c:'#C0392B'}].map((s, i, arr) => (
        <Box key={i} style={{ flexDirection:'row', alignItems:'center', flex:1 }}>
          <Box style={{ flex:1, background:s.c, borderRadius:10, padding:'16px 14px', alignItems:'center' }}>
            <Text style={{ fontSize:20, fontWeight:'bold', color:'#FFFFFF' }}>{s.s}</Text>
            <Text style={{ fontSize:15, color:'#FFFFFF', marginTop:6, textAlign:'center' }}>{s.d}</Text>
          </Box>
          {i < arr.length - 1 && <Text style={{ fontSize:28, color:'#CBD5E1', fontWeight:'bold' }}>›</Text>}
        </Box>
      ))}
    </Box>
    <Box style={{ background:'#F4F8FA', borderRadius:12, padding:'18px 22px' }}>
      <Text style={{ fontSize:20, fontWeight:'bold', color:'#1A5F7A' }}>提示词（改尖括号即可用）</Text>
      <Text style={{ fontSize:18, color:'#1F2937', marginTop:10, lineHeight:1.6, background:'#FFFFFF', borderRadius:8, padding:'14px 18px' }}>你是一位有 10 年教龄的&lt;学科&gt;教师。请把&lt;年级&gt;&lt;单元&gt;的所有知识点，设计成一张从易到难的学习路径图，每个台阶标出检验方式。分成「起点—概念理解—基本应用—迁移探究—终点证据」五级。</Text>
    </Box>
  </Box>
  <Box style={{ marginTop:14, background:'#FFF7ED', borderRadius:10, padding:'13px 20px' }}>
    <Text style={{ fontSize:18, color:'#1F2937', textAlign:'center' }}>AI 出的路径图必须自己改　——　至少改 3 处，那 3 处就是你的教学判断</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>13 / 32</Text>
  </Box>
</Slide>
