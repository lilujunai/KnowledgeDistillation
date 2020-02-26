import torch.nn as nn
import torch
import tqdm


def split_student_teacher_data(batch_data):
    return batch_data[0:5], batch_data[5:]


def knowledge_distillation(teacher_model: nn.Module, student_model: nn.Module, train_data, evaluate_data,
                           loss_model: nn.Module, optimizer, evaluator, num_epoch: int, split_data=None):
    teacher_model.eval()
    for epoch in range(num_epoch):
        for step, batch_data in enumerate(train_data):
            # split_data is a function that split train data to teacher and student
            if split_data:
                teacher_batch_data, student_batch_data = split_data(batch_data)
                with torch.no_grad():
                    teacher_output = teacher_model.forward(*teacher_batch_data)
                student_output = student_model.forward(*student_batch_data)
            else:
                with torch.no_grad():
                    teacher_output = teacher_model.forward(*batch_data)
                student_output = student_model.forward(*batch_data)

            # get loss
            loss = loss_model.forward(teacher_output, student_output, batch_data)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            evaluator.evaluate(teacher_model, student_model, evaluate_data, epoch, step)


if __name__ == "__main__":
    pass
    # a = list(range(10000))
    #
    # for i in tqdm(a, desc="Iteration", ascii=True):
    #     print(i)