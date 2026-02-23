import Sidebar from '../sidebar/Sidebar';
import CourseCard from '../ui/CourseCard';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import './style.css'
import { useContext, useEffect } from 'react';

import { SkillContext } from '../context/SkillContext';
import { SkillContextType } from '../../@types/types';
import { useNavigate } from 'react-router-dom';

const Catalogue = () =>
{

  const navigate = useNavigate()

  const context = useContext<SkillContextType>(SkillContext);

  useEffect(() => {
    if(context.user === null) {
      navigate('/auth')
    }
    else {
      fetch('http://62.113.104.103:9000/api/courses')
      .then(
        res => res.json()
      )
      .then(
        data => {
          console.log(data)
          context.setCourses(data)
        }
      )
    }
  }, [])

  return(
    <div className='container'>
    <Sidebar name="Artjom" surname="Safonov" highlight={2}/>
    <div className='catalogue'>
      <div className='options'>
        <h1 style={{ color: "#fff", margin: 0 }}>Курсы</h1>
        <div className='filters'>
          <Box sx={{ width: 120 }}>
            <FormControl fullWidth size="small" sx={{ transitionDuration: 0 }}>
              <InputLabel id="demo-simple-select-label" sx={{ fontSize: '12px', color: "#999999" }}>Фильтры</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                // value={}
                label="filters"
                // onChange={handleChange}
                sx={{ fontSize: '12px' }}
              >
                <MenuItem value={10}>Ten</MenuItem>
                <MenuItem value={20}>Twenty</MenuItem>
                <MenuItem value={30}>Thirty</MenuItem>
              </Select>
            </FormControl>
          </Box>    
        </div>
      </div>
      {/* <div className='filters'>
        <Button variant='outlined'>По моему профилю</Button>
        <Button variant='outlined'>По популярности</Button>
        <Button variant='outlined'>По вакансии</Button>
      </div> */}
      <div className='gallery'>
        {
          context.courses.map((course, index) => {
            return <CourseCard key={index} title={course.name} info={course.desc} spec={course.keywords.join(' ')}  id={course._id} rating={course.rating}/>
          })
        }
        {/* <CourseCard title="Фуллстак за 5 дней" info="Вау!" spec="Fullstack"/>
        <CourseCard title="React всего за {dayCount} дней" info="Реакт и реакт и рекат..." spec="React Frontend Web"/>
        <CourseCard title="Только для умных" info="Based and red pilled" spec="C C++ D Rust"/>
        <CourseCard title="Фуллстак за 5 дней" info="Вау!" spec="Fullstack"/>
        <CourseCard title="React всего за {dayCount} дней" info="Реакт и реакт и рекат..." spec="React Frontend Web"/>
        <CourseCard title="Только для умных" info="Based and red pilled" spec="C C++ D Rust"/> */}
      </div>
    </div>
  </div>
  )
}

export default Catalogue;