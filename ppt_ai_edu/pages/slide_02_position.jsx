<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>课程定位</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>这不是一场通用讲座，内容按县域学段与学科准备</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1.1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>五个班型，一套内容</Text>
      <Box style={{ marginTop:12, gap:9 }}>
        {[['基础班（通识）','全体教师','3-6 学时'],
          ['学科班','学科骨干','12 学时'],
          ['进阶班（新技术）','骨干 / 青年教师','6 学时'],
          ['教研班','教研组长 / 骨干','12 学时'],
          ['管理班','班主任 / 德育','6 学时']].map((r, i) => (
          <Box key={i} style={{ flexDirection:'row', alignItems:'center', background:'#FFFFFF', borderRadius:8, padding:'10px 14px' }}>
            <Text style={{ fontSize:17, fontWeight:'bold', color:'#1F2937', width:200 }}>{r[0]}</Text>
            <Text style={{ fontSize:16, color:'#5B6B7B', flex:1 }}>{r[1]}</Text>
            <Text style={{ fontSize:16, color:'#F57C00', fontWeight:'bold' }}>{r[2]}</Text>
          </Box>
        ))}
      </Box>
    </Box>
    <Box style={{ flex:1, flexDirection:'column', gap:12 }}>
      <Box style={{ flex:1, background:'#1A5F7A', borderRadius:12, padding:'18px 20px', justifyContent:'center' }}>
        <Text style={{ fontSize:34, fontWeight:'bold', color:'#FFFFFF', fontFamily:'Arial' }}>30%</Text>
        <Text style={{ fontSize:19, color:'#CFE3EA', marginTop:4 }}>讲座</Text>
      </Box>
      <Box style={{ flex:1, background:'#2E7D32', borderRadius:12, padding:'18px 20px', justifyContent:'center' }}>
        <Text style={{ fontSize:34, fontWeight:'bold', color:'#FFFFFF', fontFamily:'Arial' }}>40%</Text>
        <Text style={{ fontSize:19, color:'#D5EBD9', marginTop:4 }}>实操</Text>
      </Box>
      <Box style={{ flex:1, flexDirection:'row', gap:12 }}>
        <Box style={{ flex:1, background:'#F57C00', borderRadius:12, padding:'18px 16px', justifyContent:'center' }}>
          <Text style={{ fontSize:30, fontWeight:'bold', color:'#FFFFFF', fontFamily:'Arial' }}>20%</Text>
          <Text style={{ fontSize:18, color:'#FDEBD0', marginTop:4 }}>工作坊 / 跟岗</Text>
        </Box>
        <Box style={{ flex:1, background:'#F57C00', borderRadius:12, padding:'18px 16px', justifyContent:'center' }}>
          <Text style={{ fontSize:30, fontWeight:'bold', color:'#FFFFFF', fontFamily:'Arial' }}>10%</Text>
          <Text style={{ fontSize:18, color:'#FDEBD0', marginTop:4 }}>成果展评</Text>
        </Box>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>02 / 32</Text>
  </Box>
</Slide>
