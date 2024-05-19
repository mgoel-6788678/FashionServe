const express = require('express');
const cors = require('cors');
const app = express();
const {spawn} = require('child_process')
const path = require('path')


app.use(cors({origin: true}));
app.use(express.json())
app.get("/", (req, res) => {
  return res.status(200).send("Hey how you doing!");
})

app.use(express.static('./DeepFashion/In-shop_Clothes_Retrieval_Benchmark/Img/img/'))

app.post("/api", (req, res) => {
  (async() => {
    try {
      const query = req.body.query;
      console.log(`Got query: ${query}`);
      const python_backend = spawn('python', ['./spacyNER2/spacyNERtest.py', query])
      python_backend.stdout.on('data', (urls)=>{
        console.log(`Python output: ${urls}`)
        res.status(200).json({data: `${urls}`})
      })

      python_backend.on('close', (code) => {
        console.log(`python process exited with code: ${code}`)
      })
      // res.status(400).json({data: "failed"});
    }catch(error) {
      console.log(`Error: ${error}`);
      res.status(400).json({error: error});
    }
  })()
})

const PORT = process.env.PORT || 4000;

app.listen(PORT, ()=> {console.log(`Server running on port ${PORT}`)});
