<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>3 小时课程时间轴：M0–M6</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>从痛点破冰到带走"三样产出"，每模块都标"主题范畴 + 核心素养 + 真实单元"三锚</Text>
  </Box>
  <Box style={{ flex:1, justifyContent:'center', alignItems:'center', marginTop:8 }}>
    <svg width='1152' height='380' viewBox='0 0 1152 380'>
      <line x1='60' y1='200' x2='1092' y2='200' stroke='#CBD5E1' strokeWidth='4' />
      {[{m:'M0',t:'15分钟',d:'痛点破冰'},
        {m:'M1',t:'20分钟',d:'工具熟悉'},
        {m:'M2',t:'30分钟',d:'写作协同'},
        {m:'M3',t:'35分钟',d:'阅读与语法'},
        {m:'M4',t:'35分钟',d:'词汇与口语'},
        {m:'M5',t:'30分钟',d:'评讲与分层'},
        {m:'M6',t:'15分钟',d:'带走三样'}].map((n, i) => {
        const x = 60 + i * 172;
        const color = i === 0 ? '#C0392B' : (i === 6 ? '#2E7D32' : '#1A5F7A');
        return (
          <g key={i}>
            <text x={x} y='150' textAnchor='middle' fontSize='22' fontWeight='bold' fill={color}>{n.m}</text>
            <text x={x} y='175' textAnchor='middle' fontSize='16' fill='#F57C00'>{n.t}</text>
            <circle cx={x} cy='200' r='17' fill={color} stroke='#FFFFFF' strokeWidth='4' />
            <text x={x} y='245' textAnchor='middle' fontSize='18' fontWeight='bold' fill='#1F2937'>{n.d}</text>
          </g>
        );
      })}
    </svg>
  </Box>
  <Box style={{ flexDirection:'row', justifyContent:'center', gap:10, marginTop:4 }}>
    <Box style={{ background:'#FCEBEA', padding:'8px 16px', borderRadius:20 }}><Text style={{ fontSize:16, color:'#C0392B', fontWeight:'bold' }}>共 180 分钟</Text></Box>
    <Box style={{ background:'#F4F8FA', padding:'8px 16px', borderRadius:20 }}><Text style={{ fontSize:16, color:'#1A5F7A' }}>学员主线：带走 ①AI 互动工具/游戏 ②AI 协同教学成品 ③提示词速查卡</Text></Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:10 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI 赋能英语教学 · 课标锚定版</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>06 / 15</Text>
  </Box>
</Slide>
