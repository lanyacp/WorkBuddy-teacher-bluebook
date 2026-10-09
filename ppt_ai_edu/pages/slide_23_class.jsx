<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #F57C00', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#C2410C' }}>班主任日常与家校沟通</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>把最碎的活交给 AI，但态度和判断必须自己拿主意</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#C2410C' }}>三个高频场景</Text>
      <Box style={{ marginTop:12, gap:10 }}>
        {[['批量评语','50 名学生一次生成，再把套话改成你平时会说的话'],
          ['家长会材料','发言稿 AI 写，态度与分寸自己定'],
          ['分场景话术','学生拖拉、成绩下滑、同事误会，各准备一套']].map((r, i) => (
          <Box key={i} style={{ background:'#FFFFFF', borderRadius:8, padding:'12px 16px' }}>
            <Text style={{ fontSize:19, fontWeight:'bold', color:'#1A5F7A' }}>{r[0]}</Text>
            <Text style={{ fontSize:17, color:'#1F2937', marginTop:4, lineHeight:1.45 }}>{r[1]}</Text>
          </Box>
        ))}
      </Box>
    </Box>
    <Box style={{ flex:1, background:'#1F2937', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:19, color:'#FBBF24', fontWeight:'bold' }}>提示词（评语批量生成）</Text>
      <Text style={{ fontSize:18, color:'#E5E7EB', marginTop:12, lineHeight:1.7 }}>你是一位班主任。请为下面 10 名学生写期末评语，每条 60 字以内，语气真诚，各自挖掘一个具体优点，避免「成绩优异、品德高尚」这类套话。学生名单与表现：&lt;粘贴，已脱敏&gt;</Text>
      <Box style={{ marginTop:14, borderTop:'1px solid #374151', paddingTop:10 }}>
        <Text style={{ fontSize:16, color:'#9CA3AF', fontStyle:'italic', lineHeight:1.5 }}>提醒：学生信息先脱敏。评语发出前，每一条都要自己读过，AI 写得再顺也不是你写的。</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>23 / 32</Text>
  </Box>
</Slide>
