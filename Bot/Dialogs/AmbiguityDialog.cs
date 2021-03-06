using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Schema;
using Microsoft.Bot.Builder.Dialogs.Choices;
using Microsoft.Recognizers.Text.DataTypes.TimexExpression;

namespace Microsoft.BotBuilderSamples.Dialogs
{
    public class AmbiguityDialog : CancelAndHelpDialog
    {
        //Zu dem CHarttyp wollen wir wechseln
        private const string DestinationStepMsgText = "Please choose one option";



        public AmbiguityDialog() : base(nameof(AmbiguityDialog))
        {
            HelpMsgText = "You are in the Ambiguity-Dialog. Please choose one of the suggested options.";
            CancelMsgText = "Cancelling the ambiguity dialog";
            //AddDialog(new TextPrompt(nameof(TextPrompt)));
            AddDialog(new ChoicePrompt(nameof(ChoicePrompt)));
            AddDialog(new ConfirmPrompt(nameof(ConfirmPrompt)));
            AddDialog(new WaterfallDialog(nameof(WaterfallDialog), new WaterfallStep[]
            {
                ChosenAttributeStepAsync,
                FinalStepAsync
            }));

            // The initial child Dialog to run.
            InitialDialogId = nameof(WaterfallDialog);
        }

        //Hier findet er raus, zu welchem Charttyp wir wechseln wollen
        private async Task<DialogTurnResult> ChosenAttributeStepAsync(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            string[] ambiguityArray = (string[]) stepContext.Options;
            var options = ambiguityArray.ToList();
            var promptOptions = new PromptOptions
            {
                Prompt = MessageFactory.Text("Please choose an option from the list. I am suggesting these options because you entered an ambiguous entity."),
                RetryPrompt = MessageFactory.Text("You have to choose an option from the list."),
                Choices = ChoiceFactory.ToChoices(options),
            };
            //var changeChartTypeDetails = (ChangeChartTypeDetails)stepContext.Options;
            //return await stepContext.EndDialogAsync(changeChartTypeDetails, cancellationToken);
            return await stepContext.PromptAsync(nameof(ChoicePrompt), promptOptions, cancellationToken);
        }


        //Hier wird best?tigt, dass wohin gewechselt wurde
        //WaterfallStepContext wird von vorherigem Step ?bernommen
        private async Task<DialogTurnResult> FinalStepAsync(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //Return the foundchoice (it is in the stepContext.Result). It Contains the picked button
            return await stepContext.EndDialogAsync(stepContext.Result, cancellationToken);
        }
    }
}