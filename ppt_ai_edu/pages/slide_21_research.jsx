<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>教研与论文课题</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>从教学实录到学术表达：一条县域教师最需要被扶一把的路</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>AI 教研员：3 轮打磨一份设计</Text>
      <Box style={{ marginTop:12, gap:10 }}>
        {[['第 1 轮','贴上你的设计，让它挑毛病'],['第 2 轮','只改重难点与提问链，让它再评'],['第 3 轮','让它生成变式活动，补齐课堂节奏']].map((r, i) => (
          <Box key={i} style={{ background:'#FFFFFF', borderRadius:8, padding:'12px 16px' }}>
            <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>{r[0]}</Text>
            <Text style={{ fontSize:17, color:'#1F2937', marginTop:4 }}>{r[1]}</Text>
          </Box>
        ))}
      </Box>
      <Text style={{ fontSize:17, color:'#5B6B7B', marginTop:14, lineHeight:1.6 }}>听课记录与评课量规也用它生成，改成本校要求的维度即可。</Text>
    </Box>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#2E7D32' }}>论文与课题三级跃迁</Text>
      <Box style={{ marginTop:14, alignItems:'center' }}>
        {[['教学实录','我今天怎么上的'],['学术表达','这个现象说明了什么'],['理论支撑','它对应哪条理论']].map((r, i) => (
          <Box key={i} style={{ flexDirection:'row', alignItems:'center', gap:12, marginBottom:8 }}>
            <Box style={{ flex:1, background:'#FFFFFF', borderRadius:8, padding:'12px 16px' }}>
              <Text style={{ fontSize:19, fontWeight:'bold', color:'#1A5F7A' }}>{r[0]}</Text>
              <Text style={{ fontSize:16, color:'#5B6B7B', marginTop:3 }}>{r[1]}</Text>
            </Box>
            {i < 2 && <Text style={{ fontSize:20, color:'#CBD5E1', fontWeight:'bold' }}>↓</Text>}
          </Box>
        ))}
      </Box>
      <Box style={{ marginTop:10, background:'#FCEBEA', borderRadius:8, padding:'12px 16px' }}>
        <Text style={{ fontSize:17, color:'#7F1D1F', lineHeight:1.55 }}>红线回扣：核心论点与论证必须自己完成，AI 参与情况要如实标注</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>21 / 32</Text>
  </Box>
</Slide>
