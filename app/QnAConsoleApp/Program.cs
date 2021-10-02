using Microsoft.Azure.CognitiveServices.Knowledge.QnAMaker;
using Microsoft.Azure.CognitiveServices.Knowledge.QnAMaker.Models;
using System;
using System.Linq;

namespace QnAConsoleApp
{
    class Program
    {
        static async System.Threading.Tasks.Task Main(string[] args)
        {
            string accountEndpoint = ""; //QnA maker resource -> Keys and endpoints -> Paste endpoint here
            string queryEndpoint = ""; //QnA maker resource -> Export template -> paste qnaRuntimeEndpoint's value here
            string accountKey = ""; //QnA maker resource -> Keys and endpoints -> Paste key1 or key2 here

            Console.WriteLine("Hello! What can I help you with");
            string question = Console.ReadLine();


            var client = new QnAMakerClient(new ApiKeyServiceClientCredentials(accountKey))
            { Endpoint = accountEndpoint };
            var kbListObj = await client.Knowledgebase.ListAllAsync();
            var kbList = kbListObj.Knowledgebases;
            if (kbList.FirstOrDefault() == null)
            {
                throw new Exception("No KBs found in the QnA Maker account");
            }

            string kbId = kbList.FirstOrDefault().Id;
            var endpointKeysObject = await client.EndpointKeys.GetKeysAsync();

            var runtimeClient = new QnAMakerRuntimeClient(new EndpointKeyServiceClientCredentials(endpointKeysObject.PrimaryEndpointKey))
            { RuntimeEndpoint = queryEndpoint };

            var response = await runtimeClient.Runtime.GenerateAnswerAsync(kbId, new QueryDTO { Question = question });
            Console.WriteLine(response.Answers.FirstOrDefault().Answer);
            Console.ReadKey();

        }
    }
}
