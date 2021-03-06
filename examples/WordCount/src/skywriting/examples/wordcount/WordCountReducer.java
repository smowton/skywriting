package skywriting.examples.wordcount;
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.*;

import skywriting.examples.grep.IncrementerCombiner;
import skywriting.examples.grep.IntWritable;
import skywriting.examples.grep.PartialHashOutputCollector;
import skywriting.examples.grep.Text;
import uk.co.mrry.mercator.task.Task;

public class WordCountReducer implements Task {

	public void invoke(InputStream[] inputs, OutputStream[] outputs, String[] args) {
		int nOutputs = outputs.length;
		int nInputs = inputs.length;
		DataInputStream[] dis = new DataInputStream[nInputs];
		DataOutputStream[] dos = new DataOutputStream[nOutputs];
		
		for(int i = 0; i < nInputs; i++) {
			dis[i] = new DataInputStream(new BufferedInputStream(inputs[i]));
		}
		
		for(int i = 0; i < nOutputs; i++) {
			dos[i] = new DataOutputStream(new BufferedOutputStream(outputs[i]));
		}

		try {
			IncrementerCombiner comb = new IncrementerCombiner();
			PartialHashOutputCollector<Text, IntWritable> outMap = new PartialHashOutputCollector<Text, IntWritable>(dos, 1, Integer.MAX_VALUE, comb);
			
			for (int i = 0; i < dis.length; i++) {
				while (true) {
					Text word = new Text();
					IntWritable value = new IntWritable();
					try {
						word.readFields(dis[i]);
						value.readFields(dis[i]);
					} catch (EOFException e) {
						break;
					}

					//System.out.println(word + " = " + value);
					outMap.collect(word, value);
				}
			}
			outMap.flushAll();
			for (DataOutputStream d : dos)
				d.close();
			
		} catch (IOException e) {
			System.out.println("IOException while running reducer");
			e.printStackTrace();
			System.exit(1);
		}

	}
	

	public static void main(String[] args) throws Exception {

		int nReducers = 2;
		int nMappers = 4;
	    InputStream[] fis = new InputStream[nMappers];
	    FileOutputStream[] fos = new FileOutputStream[1];
	
	    for (int i = 0; i < nReducers; i++) {
	    
		    for (int j = 0; j < nMappers; j++) {
		    	fis[j] = new FileInputStream("wc_map_out_" + j + "_" + i);
		    }
	    	fos[0] = new FileOutputStream("wc_reduce_out_" + i);
	
		    WordCountReducer m = new WordCountReducer();
		    m.invoke(fis, fos, args);
	    }
	}
}



