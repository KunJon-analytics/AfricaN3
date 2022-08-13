import axios from "axios";

export const getQuizListData = async () => {
  try {
    const { data } = await axios.get("http://127.0.0.1:8000/api/trivia/");

    return data;
  } catch (error) {
    console.log(error);
  }
};

export const getQuizDetailData = async (triviaId) => {
  try {
    const { data } = await axios.get(
      `http://127.0.0.1:8000/api/trivia/${triviaId}`
    );

    return data;
  } catch (error) {
    console.log(error);
  }
};

export const createQuiz = async (quizData) => {
  try {
    const { data } = await axios.post(
      "http://127.0.0.1:8000/api/trivia/create/",
      quizData
    );
    return data;
  } catch (error) {
    console.log(error);
  }
};
