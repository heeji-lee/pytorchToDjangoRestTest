# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import ImageSerializer
# import torch
# from torchvision import transforms, models
# from PIL import Image
# import io
# from torch import nn
# import numpy as np
# import torch.nn.functional as F
# # import libmr
#
# #OpenMax, 이용
# # #1
# # class WeibullFitting:
# #     def __init__(self, tailsize=20):
# #         self.tailsize = tailsize
# #         self.weibull_models = {}
# #
# #     def fit(self, activations, labels):
# #         unique_labels = np.unique(labels)
# #         for label in unique_labels:
# #             class_activations = activations[labels == label]
# #             mean_vec = np.mean(class_activations, axis=0)
# #             distances = np.linalg.norm(class_activations - mean_vec, axis=1)
# #             mr = libmr.MR()
# #             mr.fit_high(distances, len(distances))
# #             self.weibull_models[label] = (mean_vec, mr)
# #
# #     def wscore(self, activations):
# #         scores = []
# #         for label, (mean_vec, mr) in self.weibull_models.items():
# #             distances = np.linalg.norm(activations - mean_vec, axis=1)
# #             wscores = mr.w_score(distances)
# #             scores.append(wscores)
# #         return np.array(scores)
# #
# # #2
# # def compute_openmax(activation_vector, weibull_model, alpha=10):
# #     ranked_activations = np.sort(activation_vector)[::-1]
# #     top_indices = np.argsort(activation_vector)[::-1][:alpha]
# #
# #     wscore = weibull_model.wscore(ranked_activations[top_indices])
# #
# #     openmax_vector = np.copy(activation_vector)
# #     openmax_vector[top_indices] -= openmax_vector[top_indices] * wscore
# #
# #     openmax_unknown_score = np.sum(activation_vector[top_indices] * wscore)
# #     openmax_vector = np.append(openmax_vector, openmax_unknown_score)
# #
# #     openmax_probs = F.softmax(torch.tensor(openmax_vector), dim=0).numpy()
# #     return openmax_probs
# #
# # #3
# # # Pretrained ResNet50 model
# # model = models.resnet50(pretrained=True)
# # model.eval()
# #
# #
# # # 이미지에서 특징 벡터 추출
# # def extract_features(image, model):
# #     with torch.no_grad():
# #         features = model(image)
# #     return features.numpy()
# #
# #
# # # Example of fitting Weibull model using activation vectors
# # def fit_weibull_for_model(train_loader, model, weibull_model):
# #     activations = []
# #     labels = []
# #
# #     for images, targets in train_loader:
# #         features = extract_features(images, model)
# #         activations.append(features)
# #         labels.append(targets.numpy())
# #
# #     activations = np.concatenate(activations, axis=0)
# #     labels = np.concatenate(labels, axis=0)
# #
# #     weibull_model.fit(activations, labels)
# #
# # #4
# # # 이미지 예측 시 OpenMax 사용
# # def predict_with_openmax(image, model, weibull_model, class_labels, alpha=10):
# #     features = extract_features(image, model)
# #
# #     openmax_probs = compute_openmax(features[0], weibull_model, alpha=alpha)
# #     predicted_class = np.argmax(openmax_probs)
# #
# #     if predicted_class == len(class_labels):  # Unknown class index
# #         return "Unknown", openmax_probs[predicted_class]
# #     else:
# #         return class_labels[predicted_class], openmax_probs[predicted_class]
# #OpenMax
#
#
# # 경로 설정
# model_weight_save_path = "pytorchToDjangoTest/resnet50_epoch_48_team1_loss_2153_acc_69_52.pth"
# num_classes = 5
#
# # ResNet-50 모델 정의 및 로드
# model = models.resnet50(pretrained=False)
# num_ftrs = model.fc.in_features
# model.fc = torch.nn.Linear(num_ftrs, num_classes)
#
# # 모델 가중치 로드
# checkpoint = torch.load(model_weight_save_path, map_location=torch.device('cpu'))
# model.load_state_dict(checkpoint, strict=False)
# model.eval()
#
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# model = model.to(device)
#
#
#
# class ImageClassificationView(APIView):
#
#     def post(self, request, *args, **kwargs):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             image = serializer.validated_data['image']
#
#             # 이미지 변환
#             transform = transforms.Compose([
#                 transforms.Resize((224, 224)),
#                 transforms.ToTensor(),
#                 transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#             ])
#
#             # 이미지 처리
#             image = Image.open(image).convert('RGB')
#             image = transform(image).unsqueeze(0).to(device)
#
#             # 예측
#             with torch.no_grad():
#                 outputs = model(image)
#                 probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
#                 _, predicted = torch.max(outputs, 1)
#                 predicted_class_index = predicted.item()
#                 # confidence = torch.nn.functional.softmax(outputs, dim=1)[0][predicted_class_index].item()
#                 confidence = probabilities[predicted_class_index].item()
#                 max_confidence, predicted = torch.max(probabilities, 0)
#
#
#                 # 1조
#                 class_labels = {0: '고양이', 1: '공룡', 2: '강아지',3: '꼬북이',4: '티벳여우'}
#                 #3조
#                 # class_labels = {0: '공구톱', 1: '공업용가위', 2: '그라인더', 3: '니퍼', 4: '드라이버'
#                 #                 , 5: '망치', 6: '스패너', 7: '전동드릴', 8: '줄자', 9: '버니어 캘리퍼스'}
#                 #2조
#                 # class_labels = {0: '업소용냉장고', 1: 'cpu', 2: '드럼세탁기', 3: '냉장고', 4: '그래픽카드', 5: '메인보드'
#                 #     , 6: '전자레인지', 7: '파워', 8: '렘', 9: '스탠드에어컨', 10: 'TV', 11: '벽걸이에어컨', 12: '통돌이세탁기'}
#
#                 # predicted_class_label = class_labels[predicted_class_index]
#                 # 정확도가 50% 미만인 경우 기타로 분류
#
#                 # OpenMax를 사용하여 예측
#                 # predicted_class, confidence = predict_with_openmax(image, model, weibull_model, class_labels)
#
#                 if max_confidence < 0.5:
#                     predicted_class_label = "기타"
#                 else:
#                     # predicted_class_label = class_labels[predicted_class_index]
#                     predicted_class_label = class_labels.get(predicted.item(), "기타")
#
#                 # 모든 클래스에 대한 확률 반환
#                 class_confidences = {class_labels[i]: round(probabilities[i].item(), 4) for i in range(num_classes)}
#
#             # 응답 데이터
#             response_data = {
#                 'predicted_class_index': predicted_class_index,
#                 'predicted_class_label': predicted_class_label,
#                 'confidence': confidence,
#                 'class_confidences': class_confidences  # 각 클래스에 대한 확률
#             }
#
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)