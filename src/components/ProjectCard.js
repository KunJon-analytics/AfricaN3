import { Col } from "react-bootstrap";

export const ProjectCard = ({ title, description, image_url, project_url }) => {
  return (
    <Col size={12} sm={6} md={4}>
      <div className="proj-imgbx">
        <a href={project_url} target="_blank" rel="noreferrer">
          <img src={image_url} alt={description} />
          <div className="proj-txtx">
            <h4>{title}</h4>
            <span>{description}</span>
          </div>
        </a>
      </div>
    </Col>
  );
};
