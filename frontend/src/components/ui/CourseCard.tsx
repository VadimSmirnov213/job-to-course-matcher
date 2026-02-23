import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import Rating from '@mui/material/Rating';

import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import ThumbDownOffAltOutlinedIcon from '@mui/icons-material/ThumbDownOffAltOutlined';
import { useState } from 'react';
import { InputLabel, TextField } from '@mui/material';

interface ICardProps {
  id: number;
  title: string;
  info: string;
  spec?: string;
  rating: number;
}

const CourseCard = ({id, title, info, spec, rating} : ICardProps) => {

  const [value, setValue] = useState<number | null>(rating);
  const [comment, setComment] = useState<string>("");

  const handleRating = (rate: number | null) => {
    console.log(rate)
    setValue(rate);
    let bodyt = JSON.stringify({
      course_id: `${id}`,
      text: comment,
      count_star: rate})
    fetch(`http://62.113.104.103:9000/api/feedback`, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json'
      },
      body: bodyt
      }
    ).then(
      res => console.log(id, bodyt)
    )
  }

  return(
    <Card variant="outlined" sx={{ width: '300px', height: 'fit-content', bgcolor: '#262626', borderColor: '#2e2e2e', borderRadius: '10px', textAlign: 'center' }}>
      <CardContent sx={{ height: '400px', cursor: 'pointer' }}>
        <CardHeader title={title}>
        </CardHeader>
        {/* <Typography variant="h5" component="div">
          {title}
        </Typography> */}
        <br />
        <Typography variant="body2">
          {info.substring(0, 100) + "..."}
        </Typography>
        <br />
        {/* <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {spec.split(/[ ,]+/).map((tag, index) => {
            <Chip key={index} />
          })}
        </Typography> */}
        {
          spec 
          &&
          <div>
            {spec?.split(/[ ,]+/).map((tag, index) => {
              return <Chip key={index} label={tag.split("'").join("")} variant='outlined' sx={{ mr: '5px', mt: '5px',color: "#8b8b8b" }}/>
            })}
          </div>
        }
      </CardContent>
      <CardActions sx={{ display: 'flex', justifyContent: 'flex-start', bgcolor: '#1e1e1e', columnGap: '10px' }}>
        <Rating
          name="simple-controlled"
          value={value}
          onChange={(event, newValue) => handleRating(newValue)}
        />
        <div style={{ display: 'block' }}>
          <InputLabel id="fname" sx={{ fontSize: '12px', color: "#999999" }}>Отзыв</InputLabel>
          <TextField id="first_name" label="" variant="outlined" value={comment} onChange={(e) => {setComment(e.target.value)}}/>
        </div> 
        {/* <ThumbUpOutlinedIcon sx={{ color: "#999999", ml: '10px', width: '20px', cursor: 'pointer' }}/>
        <ThumbDownOffAltOutlinedIcon sx={{ color: '#999999', width: '20px', cursor: 'pointer' }}/> */}
      </CardActions>
    </Card>
  )
}

export default CourseCard;