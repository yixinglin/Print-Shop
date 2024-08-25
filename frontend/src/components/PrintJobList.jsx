import React, { useState, useEffect } from "react";
import { Table, Tag, Space } from "antd";

// 示例数据
const exampleJobs = [
  {
    job_id: 1,
    number_of_documents: 3,
    job_media_progress: "50%",
    copies: 2,
    media: "A4",
    page_set: "all",
    print_color_mode: "color",
    print_scaling: "fit",
    time_at_creation: "2024-08-25 12:30:00",
    job_state: "printing",
    job_state_reasons: ["none"],
    document_name_supplied: "example1.pdf",
  },
  {
    job_id: 2,
    number_of_documents: 1,
    job_media_progress: "100%",
    copies: 1,
    media: "A3",
    page_set: "all",
    print_color_mode: "monochrome",
    print_scaling: "none",
    time_at_creation: "2024-08-25 13:00:00",
    job_state: "completed",
    job_state_reasons: ["completed-successfully"],
    document_name_supplied: "example2.pdf",
  },
  // 其他示例任务
];

const PrintJobList = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    // 假设从API获取数据
    // setJobs(dataFromAPI);
    setJobs(exampleJobs); // 使用示例数据
  }, []);

  const columns = [
    {
      title: "Job ID",
      dataIndex: "job_id",
      key: "job_id",
    },
    {
        title: "Created At",
        dataIndex: "time_at_creation",
        key: "time_at_creation",
      },
    {
        title: "Document Name",
        dataIndex: "document_name_supplied",
        key: "document_name_supplied",
      },
    {
      title: "#Documents",
      dataIndex: "number_of_documents",
      key: "number_of_documents",
    },
    {
      title: "Progress",
      dataIndex: "job_media_progress",
      key: "job_media_progress",
    },
    {
      title: "Copies",
      dataIndex: "copies",
      key: "copies",
    },

    {
        title: "Job State",
        dataIndex: "job_state",
        key: "job_state",
        render: (text) => {
          let color = text === "completed" ? "green" : "blue";
          if (text === "printing") {
            color = "geekblue";
          } else if (text === "canceled") {
            color = "volcano";
          }
          return (
            <Tag color={color} key={text}>
              {text.toUpperCase()}
            </Tag>
          );
        },
      },
      {
        title: "Job State Reasons",
        dataIndex: "job_state_reasons",
        key: "job_state_reasons",
        render: (reasons) => (
          <>
            {reasons.map((reason) => {
              let color = reason === "completed-successfully" ? "green" : "volcano";
              return (
                <Tag color={color} key={reason}>
                  {reason.toUpperCase()}
                </Tag>
              );
            })}
          </>
        ),
      },
      
    {
      title: "Media",
      dataIndex: "media",
      key: "media",
    },
    {
      title: "Page Set",
      dataIndex: "page_set",
      key: "page_set",
    },
    {
      title: "Color Mode",
      dataIndex: "print_color_mode",
      key: "print_color_mode",
    },
    {
      title: "Scaling",
      dataIndex: "print_scaling",
      key: "print_scaling",
    },



  ];

  return (
    <Table columns={columns} dataSource={jobs} rowKey="job_id" />
  );
};

export default PrintJobList;
