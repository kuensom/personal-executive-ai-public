# OpenAI API setup

## 1. Create an API key

Sign in to the OpenAI developer platform, select or create a project, and create an API key. Treat the key as a secret; it may permit billable requests.

## 2. Add API credit and limits

ChatGPT subscriptions do not include OpenAI API credit. Configure API billing and consider setting project-level spending controls suitable for your use.

## 3. Configure the application

Add the following to your local `.env`:

```dotenv
OPENAI_API_KEY=replace-with-your-own-key
OPENAI_MODEL=gpt-5.6-luna
```

The documented implementation used `gpt-5.6-luna` as a cost-conscious model. Model availability and pricing can change; select a currently available model that meets the response-quality and cost requirements of your deployment.

## 4. Verify without exposing the key

Run the project's integration check or complete workflow. Do not use `echo $OPENAI_API_KEY`, commit `.env`, or include the key in screenshots.

If the application reports authentication failure:

1. verify the key belongs to the intended API project;
2. confirm `.env` is being loaded;
3. confirm the project has available credit;
4. create a replacement key if exposure is suspected;
5. revoke the old key after replacement.

## Cost and privacy considerations

- Email and calendar-derived content sent to the model may be sensitive.
- Review the provider's current data controls and retention terms for your API account.
- Minimise the content sent to the model.
- Avoid logging full prompts or model inputs by default.
- Use token and cost reporting to detect unexpected usage.
