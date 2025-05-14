import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function ModalitiesChart({ data }) {
  // data = [
  //   { name: 'Metin', value: 85 },
  //   { name: 'Ses',   value: 70 },
  //   { name: 'Yüz',   value: 50 }
  // ]
  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis domain={[0, 100]} tickFormatter={v => `${v}%`} />
        <Tooltip formatter={value => `${value}%`} />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
}
