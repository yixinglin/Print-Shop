import React, { useState } from 'react';
import { Form, Input, Button, Select, InputNumber, Radio } from 'antd';

const PrintJobForm = ({title, formValues, formOptions, key, onFinish }) => {
    const { mediaSizes, colorModes } = formOptions;
    
    var defaultValues = {
        copies: 1,
        paperSize: "iso_a4_210x297mm",
        colorMode: "monochrome",
        printScaling: "",
        pageSet: "all"
    }
    if (formValues) {
        defaultValues = formValues;
    }

    return <Form
        key={key}
        name="create-job"
        id="create-job-form"
        layout="vertical"
        onFinish={onFinish}
        initialValues={{
            title,
            ...defaultValues,
        }}
        style={{ maxWidth: '600px' }}
    >
        <p>💡 Please enter the details for your print job</p>

        <Form.Item
            label="Job Title"
            name="title"
            rules={[{ required: true, message: 'Please enter a job title!' }]}
        >
            <Input placeholder="Enter job title" />
        </Form.Item>

        <Form.Item
            label="Page Range"
            name="pageRange"
            tooltip="Specify pages like 1-5 or 1,3,5"
        >
            <Input placeholder="Enter page range (e.g., 1-5, 8)" />
        </Form.Item>
        <Form.Item
            label="Copies"
            name="copies"
            rules={[{ required: true, message: 'Please enter number of copies!' }]}
        >
            <InputNumber min={1} />
        </Form.Item>

        <Form.Item
            label="Paper Size"
            name="paperSize"
            rules={[{ required: true, message: 'Please select a paper size!' }]}
        >
            <Select placeholder="Select paper size">
                {mediaSizes.map((size, index) =>
                    <Option key={index} value={size}>{size}</Option>)}
            </Select>
        </Form.Item>

        <Form.Item
            label="Color"
            name="colorMode"
            rules={[{ required: true, message: 'Please select a color!' }]}
        >
            <Select placeholder="Select color">
                {colorModes.map((mode, index) =>
                    <Option key={index} value={mode}>{mode}</Option>)}
            </Select>
        </Form.Item>
        <Form.Item
            label="Page Set"
            name="pageSet"
            tooltip="Select a page set to print"
        >
            <Radio.Group size="small">
                <Radio value="all">All</Radio>
                <Radio value="odd">Odd</Radio>
                <Radio value="even">Even</Radio>
            </Radio.Group>
        </Form.Item>
        <Form.Item
            label="Scale"
            name="printScaling"
            tooltip="Select a print scaling option"
        >
            <Radio.Group size="small">
                <Radio value="">None</Radio>
                <Radio value="auto">Auto</Radio>
                <Radio value="fit">Fit</Radio>
                <Radio value="fill">Fill</Radio>
            </Radio.Group>
        </Form.Item>
        <Form.Item>
            <Button type="primary" htmlType="submit">
                Start to Print
            </Button>
        </Form.Item>
    </Form>

}


export default PrintJobForm;