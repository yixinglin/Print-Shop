import React, { useEffect, useState } from "react";
import PrintJobList from '../components/PrintJobList.jsx';
import { fetch_job_attributes, fetch_jobs, delete_all_jobs } from '../rest/printer.js';
import { Button, Space } from 'antd';

const PrintJobListView = () => {

  const [printJobs, setPrintJobs] = useState(null);

  const fetchPrintJobs = async () => {
    const ans = await fetch_jobs();
    const jobs = ans.data.jobs;
    const attrs = []
    console.log(jobs);
    for (const [job_id, job_uri] of Object.entries(jobs)) {
      const job_attrs = await fetch_job_attributes(job_id);
      attrs.push(job_attrs.data.job_attributes);
    }
    return new Promise((resolve, reject) => {
      resolve(attrs);
      reject(new Error("Failed to fetch print jobs"));
    });
  }


  useEffect(() => {
    console.log("PrintJobListView: Fetching print jobs");
    fetchPrintJobs().then(jobs => {
      console.log("PrintJobListView: Print jobs fetched", jobs);
      // setPrintJobs(jobs);
      const foFill = jobs.map(job => {
        // Timestamp 1724608162 to string, yyyy-mm-dd hh:mm:ss
        const time_str = new Date(job['time-at-creation'] * 1000)
          .toISOString().replace('T', '').slice(0, 19);
        return {
          job_id: job['job-id'],
          copies: job['copies'],
          media: job['media'],
          page_set: job['page-set'],
          print_color_mode: job['print-color-mode'],
          print_scaling: job['print-scaling'],
          time_at_creation: time_str,
          job_state: jobStateToName[job['job-state']] || 'unknown',
          job_state_reasons: [job['job-state-reasons']] || [],
          document_name_supplied: job['document-name-supplied'],
        }
      });
      console.log(foFill);
      setPrintJobs(foFill);

    }).catch(err => {
      console.error(err);
    });

  }, []);

  const handleDeleteAll = () => {
    delete_all_jobs();
    handleRefresh();
  }

  const handleRefresh = () => {
    window.location.reload();
  }

  return (
    <div>
      <h1>🌊✮ ⋆ 🦈｡ * ⋆｡</h1>
      <h1>Print Jobs</h1>
      <Space direction="horizontal">
        <Button type="primary" onClick={() => { handleRefresh(); }}>Refresh</Button>
        <Button type="default" onClick={() => { handleDeleteAll(); }} danger>Clear</Button>
      </Space>
      <PrintJobList jobs={printJobs} />
    </div>
  )
}

// pycups job-state to job-state-name mapping
const jobStateToName = {
  3: 'pending',
  4: 'held',
  5: 'processing',
  6: 'stopped',
  7: 'canceled',
  8: 'aborted',
  9: 'completed',
  10: 'completed-with-errors',
  11: 'deleted',
}

export default PrintJobListView;