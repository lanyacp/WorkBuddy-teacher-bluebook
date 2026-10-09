<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>考核与 21 天打卡</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>不设笔试，用过程打卡和真实产出替代</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:16, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>三层考核</Text>
      <Box style={{ marginTop:14, gap:11 }}>
        {[['过程考核','每个板块的实操任务打卡','不发笔试'],['结业产出','每人 1 份「AI 赋能教学案例」','含前后对比'],['骨干产出','骨干另交 1 个自建 Skill','教研组内共享']].map((r, i) => (
          <Box key={i} style={{ background:'#FFFFFF', borderRadius:8, padding:'13px 16px' }}>
            <Text style={{ fontSize:20, fontWeight:'bold', color:'#2E7D32' }}>{r[0]}</Text>
            <Text style={{ fontSize:17, color:'#1F2937', marginTop:4 }}>{r[1]}</Text>
            <Text style={{ fontSize:15, color:'#94A3B8', marginTop:3 }}>{r[2]}</Text>
          </Box>
        ))}
      </Box>
    </Box>
    <Box style={{ flex:1.1, background:'#1F2937', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#FBBF24' }}>21 天行动打卡</Text>
      <Text style={{ fontSize:18, color:'#E5E7EB', marginTop:10, lineHeight:1.65 }}>第 1 周 上手：写出第一条指令、备一次课、建一份问卷<br />第 2 周 用起来：做评语、做教研员迭代、建自己的模板<br />第 3 周 留下来：整理学科提示词卡、写结业案例初稿</Text>
      <Box style={{ marginTop:14, borderTop:'1px solid #374151', paddingTop:10 }}>
        <Text style={{ fontSize:16, color:'#9CA3AF', fontStyle:'italic', lineHeight:1.5 }}>每天只做一件小事。21 天后这张表就是你的成果证明，也是你评职称时能拿出来的过程性材料。</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>31 / 32</Text>
  </Box>
</Slide>
